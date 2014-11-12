from imagr import views
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from imagr_user.views import ActivationView, RegistrationView
from django.contrib.auth import views as auth_views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'imagr_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^home[/]?$', views.home, name='home'),
    url(r'^album/(?P<pk>\d+)/$', views.AlbumView.as_view(), name='album'),
    url(r'^photo/(?P<pk>\d+)/$', views.photo, name='photo'),
    url(r'^photo/(?P<pk>\d+)/details$', views.PhotoDetails.as_view(),
        name='photo_details'),
    url(r'^stream[/]?$', views.stream, name='stream'),
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='imagr_user/activation_complete.html'),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(template_name='imagr_user/activate.html'),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(template_name='imagr_user/registration_form.html'),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='imagr_user/registration_complete.html'),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(template_name='imagr_user/registration_closed.html'),
        name='registration_disallowed'),
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'imagr_user/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'imagr_user/logout.html'},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^upload_photo/$', 
        views.UploadPhotoView.as_view(), name='upload_photo')
)
