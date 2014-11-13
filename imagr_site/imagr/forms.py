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
        self.fields['album_field'] = forms.MultipleChoiceField(choices=choices)

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
