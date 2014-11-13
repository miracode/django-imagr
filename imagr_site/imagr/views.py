from django.shortcuts import render, redirect
# from django.http import HttpResponse
from imagr.models import Album, Photo
from django.views import generic
from django.views.generic.edit import FormView
from django.utils import timezone
import datetime
from imagr.forms import UploadPhotoForm, AddPhotoForm


def index(request):
    return render(request, 'imagr/index.html')


def home(request):
    user = request.user
    album_list = Album.objects.filter(owner__pk=user.pk)
    context = {'albums': album_list,
               'user': user, }
    return render(request, 'imagr/home.html', context)


class AlbumView(generic.DetailView):
    model = Album
    template_name = 'imagr/album.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['form'] = AddPhotoForm(user=self.request.user,
                                       album_id=context['album'].pk)
        return context


def photo(request, pk):
    return redirect('http://imagr.jasonbrokaw.com/%s' % pk)


class PhotoDetails(generic.DetailView):
    model = Photo
    template_name = 'imagr/photo_details.html'


def stream(request):
    user = request.user
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


class UploadPhotoView(FormView):
    template_name = 'imagr/photo_upload.html'
    form_class = UploadPhotoForm

    def get_form_kwargs(self):
        kwargs = super(UploadPhotoView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('/imagr/home/')
