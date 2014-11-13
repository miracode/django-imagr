from django.forms import ModelForm
from django import forms
from imagr.models import Photo, Album
from django.utils import timezone
import aws_bucket


class UploadPhotoForm(ModelForm):
    photo_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        albums = Album.objects.filter(owner=self.user.pk)
        choices = [(album.pk, album.title) for album in albums]
        super(UploadPhotoForm, self).__init__(*args, **kwargs)
        album_field = forms.MultipleChoiceField(choices=choices)
        album_field.label = "Add to Albums"
        album_field.required = False
        self.fields['album_field'] = album_field

    class Meta:
        model = Photo
        fields = ['title', 'description', 'photo_file', 'published']

    def save(self, commit=True):
        now = timezone.now()
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        owner = self.user
        published = self.cleaned_data['published']
        file_size = (self.cleaned_data['photo_file'].size / (2.0 ** 20))
        album_ids = self.cleaned_data['album_field']

        photo = Photo(title=title, description=description,
                      date_uploaded=now, published=published, owner=owner,
                      file_size=file_size)
        photo.save()

        albums = Album.objects.filter(id__in=album_ids)

        for album in albums:
            album.photos.add(photo)

        aws_bucket.upload_photo(photo.pk, self.cleaned_data['photo_file'])


class AddPhotoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.album = Album.objects.get(id=kwargs.pop('album_id'))
        photos = Photo.objects.filter(owner=self.user.pk)
        choices = [(photo.pk, photo.title) for photo in photos
                   if self.album not in photo.album_set.all()]
        super(AddPhotoForm, self).__init__(*args, **kwargs)
        photo_field = forms.MultipleChoiceField(choices=choices)
        photo_field.label = "Add Photos to this Album"
        photo_field.required = False
        self.fields['photo_field'] = photo_field

    fields = ['photo_field']
