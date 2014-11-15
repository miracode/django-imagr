from fabric.api import task, cd, run, env, prompt, execute, sudo, open_shell
from fabric.api import settings, put
import fabric.contrib
import time
import os
# import io
import boto
import boto.ec2

env.hosts = ['localhost', ]
env["user"] = "ubuntu"
env["key_filename"] = "~/.ssh/pk-aws.pem"
env.aws_region = 'us-west-2'


@task
def host_type():
    run('uname -s')


def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


@task
def provision_instance(wait_for_running=False, timeout=60,
                       interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't2.micro'
    key_name = 'mykeypair'
    security_group = 'ssh-access'
    image_id = "ami-3d50120d"
    # subnet_id = create_network()  # Probably don't want to do this each time

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ],
    )
    new_instances = [i for i in reservations.instances
                     if i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()

    elastic_ip = conn.allocate_address(domain="vpc")
    conn.associate_address(instance_id=reservations.instances[0].id,
                           allocation_id=elastic_ip.allocation_id)


@task
def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        env.user + '@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


def _install_imagr_requirements():
    sudo('apt-get update')
    sudo('apt-get -y upgrade')
    sudo('apt-get -y install python-pip')
    sudo('apt-get -y install python-dev')
    sudo('apt-get -y install postgresql-9.3')
    sudo('apt-get -y install postgresql-server-dev-9.3')
    sudo('apt-get -y install git')

    if not fabric.contrib.files.exists('~/django-imagr/'):
        with settings(warn_only=True):
            sudo('git clone https://github.com/miracode/django-imagr.git')
    with cd('django-imagr'):
        sudo('pip install -r requirements.txt')


def _setup_database():
    # Set this environment variable on local machine before running this!
    password = os.environ['DATABASE_PASSWORD']
    create_user_command = """"
  create user imagr with password '%s';
  grant all on database imagr to imagr;"
""" % password
    with settings(warn_only=True):
        sudo('createdb imagr', user='postgres')
    sudo('psql -U postgres imagr -c %s' % create_user_command, user='postgres')


def _start_server():
    secrets_file_name = \
        raw_input("Enter the name & path for the secrets.sh file: ")
    env.secrets_file = put(secrets_file_name, '.')[0]
    boto_file_name = raw_input("Enter the name & path for the .boto file: ")
    if not fabric.contrib.files.exists('~/.boto'):
        boto_file_name = put(boto_file_name, '.')[0]
    if not fabric.contrib.files.exists('~/.boto'):
        sudo('mv %s ~/.boto' % boto_file_name)
    sudo('chmod 400 .boto')
    with cd('django-imagr/imagr_site'):
        sudo('source ../../%s && python manage.py migrate' % env.secrets_file)
        sudo('source ../../%s && gunicorn -b 0.0.0.0:80 imagr_site.wsgi:application'
             % env.secrets_file)

def _refresh_django_app():
    with cd('~/django-imagr'):
        sudo('git pull origin master')
    secrets_file_name = \
        raw_input("Enter the name & path for the secrets.sh file: ")
    env.secrets_file = put(secrets_file_name, '.')[0]
    with cd('~/django-imagr/imagr_site'):
        sudo('source ../../%s && python manage.py migrate' % env.secrets_file)

def _install_nginx():
    sudo('apt-get install nginx')
    sudo('/etc/init.d/nginx start')


@task
def refresh_django_app():
    run_command_on_selected_server(_refresh_django_app)

@task
def install_django_imagr():
    run_command_on_selected_server(_install_imagr_requirements)


@task
def setup_imagr_database():
    run_command_on_selected_server(_setup_database)


@task
def start_server():
    run_command_on_selected_server(_start_server)


@task
def install_nginx():
    run_command_on_selected_server(_install_nginx)


@task
def ssh():
    run_command_on_selected_server(open_shell)


@task
def stop_instance():
    select_instance()
    conn = get_ec2_connection()
    conn.stop_instances(instance_ids=[env.active_instance.id])


@task
def terminate_instance():
    select_instance(state="stopped")
    conn = get_ec2_connection()
    conn.terminate_instances(instance_ids=[env.active_instance.id])


@task
def release_address():
    conn = get_ec2_connection()
    prompt_text = "Please select from the following addresses:\n"
    address_template = " %(ct)d: %(id)s\n"
    addresses = conn.get_all_addresses()
    for idx, address in enumerate(addresses):
        ct = idx + 1
        args = {'ct': ct, 'id': str(address)}
        prompt_text += address_template % args
    prompt_text += "Choose an address: "

    def validation(input):
        choice = int(input)
        if not choice in range(1, len(addresses) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    addresses[choice - 1].release()


### Dan's stuff down here for ref.
# from fabric.api import local
#
#
# def create_network():
#     vpc_connection = boto.connect_vpc()
#     vpc = vpc_connection.create_vpc("10.0.0.0/24")
#     subnet = vpc_connection.create_subnet(vpc.id, "10.0.0.0/25")
#     gateway = vpc_connection.create_internet_gateway()
#     vpc_connection.attach_internet_gateway(gateway.id, vpc.id)
#     return subnet.id


# def create_server(subnet_id):
#     ec2_connection = get_ec2_connection()
#     reservation = ec2_connection.run_instances("ami-3d50120d",
#                                                key_name="fabric",
#                                                instance_type="t2.micro",
#                                                subnet_id=subnet_id)
#     print "Sleeping while EC2 nodes come up..."
#     time.sleep(60)
#     print "done\n"
#     elastic_ip = ec2_connection.allocate_address(domain="vpc")
#     ec2_connection.associate_address(instance_id=reservation.instances[0].id,
#                                      allocation_id=elastic_ip.allocation_id)
#     return elastic_ip.public_ip


# @task
# def checkpoint():
#     local("python ./manage.py makemigrations")
#     local("git add .")
#     local("git commit")


# @task
# def deploy_node():
#     subnet_id = create_network()
#     node_ip = create_server(subnet_id)
#     print node_ip
#     env["hosts"] = [node_ip]
