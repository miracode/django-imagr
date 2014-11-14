import boto


def upload_photo(key_id, photo_file):
    s3 = boto.connect_s3()
    bucket = s3.get_bucket('imagr.jasonbrokaw.com')
    k = boto.s3.key.Key(bucket)
    k.key = str(key_id)
    k.set_contents_from_file(photo_file)
