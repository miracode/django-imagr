from django.shortcuts import render, redirect
# from django.http import HttpResponse
from imagr.models import Album, Photo, ImagrUser
from django.views import generic
from django.views.generic.edit import FormView
from django.utils import timezone
import datetime
from imagr.forms import UploadPhotoForm, AddPhotoForm, AlbumForm, FollowForm


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

    def post(self, request, **kwargs):
        album_id = kwargs.pop('pk')
        photo_id = request.POST['photo_field']
        photo = Photo.objects.get(id=photo_id)
        Album.objects.get(id=album_id).photos.add(photo)
        return redirect(request.path)


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


class CreateAlbumView(FormView):
    template_name = 'imagr/create_album.html'
    form_class = AlbumForm

    def get_form_kwargs(self):
        kwargs = super(CreateAlbumView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('/imagr/home/')


class ProfileView(generic.DetailView):
    model = ImagrUser
    template_name = 'imagr/profile.html'
    success_url = '/imagr/profile/'

    def get_object(self):
        self.form = FollowForm(instance=self.request.user)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(
            pk=self.request.user.pk, **kwargs)
        context['form'] = self.form
        return context

    def post(self, request, **kwargs):
        self.form.save(request.POST)
        return redirect('/imagr/profile/')
