import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

PUBLISHED_CHOICES = (
    ('private', 'This is private'),
    ('shared', 'This is shared'),
    ('public', 'This is public'),
)


class ImagrUser(AbstractBaseUser):
    #following =
    pass


class Photo(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified')
    date_published = models.DateTimeField('date published')
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of photo")


class Album(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified')
    date_published = models.DateTimeField('date published')
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of album")
    cover_photo = models.ForeignKey(Photo, related_name="cover_photo")
    photos = models.ManyToManyField(Photo, verbose_name="photos in album",
                                    limit_choices_to={'owner': owner})
