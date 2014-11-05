from django.shortcuts import render
from django.http import HttpResponse
from imagr.models import Album, Photo, ImagrUser
from django.views import generic
from django.utils import timezone
import datetime


def index(request):
    return render(request, 'imagr/index.html')


def home(request):
    # user = request.user
    user = ImagrUser.objects.all()[0]
    album_list = Album.objects.filter(owner__pk=user.pk)
    context = {'albums': album_list,
               'user': user, }
    return render(request, 'imagr/home.html', context)


class AlbumView(generic.DetailView):
    model = Album
    template_name = 'imagr/album.html'


def photo(request, pk):
    return HttpResponse('X')


class PhotoDetails(generic.DetailView):
    model = Photo
    template_name = 'imagr/photo_details.html'


def stream(request):
    # user = request.user
    user = ImagrUser.objects.all()[0]
    our_recent_photos = Photo.objects.filter(
        owner=user,
        date_published__gt=timezone.now() - datetime.timedelta(days=5))

    friends_recent_photos = []
    for friend in user.following.all():
        for photo in friend.photos.all():
            if photo.was_published_recently:
                friends_recent_photos.append(photo)
    context = {'user': user,
               'recent_photos': our_recent_photos,
               'friends_photos': friends_recent_photos}
    return render(request, 'imagr/stream.html', context)
