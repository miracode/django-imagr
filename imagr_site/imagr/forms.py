from django.forms import ModelForm
from django import forms
from imagr.models import Photo
from django.utils import timezone
import aws_bucket


class UploadPhotoForm(ModelForm):
    photo_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UploadPhotoForm, self).__init__(*args, **kwargs)

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

        photo = Photo(title=title, description=description,
                      date_uploaded=now, published=published, owner=owner,
                      file_size=file_size)
        photo.save()

        aws_bucket.upload_photo(photo.pk, self.cleaned_data['photo_file'])
