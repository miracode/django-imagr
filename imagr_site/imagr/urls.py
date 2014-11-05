from imagr import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'imagr_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^home[/]?$', views.home, name='index'),
    url(r'^album/(?P<pk>\d+)/$', views.AlbumView.as_view(), name='album'),
    url(r'^photo/(?P<pk>\d+)/$', views.photo, name='photo'),
    url(r'^photo/(?P<pk>\d+)/details$', views.PhotoDetails.as_view(),
        name='photo_details'),
    url(r'^stream[/]?$', views.stream, name='stream'),
)
