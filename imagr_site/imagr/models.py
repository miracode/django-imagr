# import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser

PUBLISHED_CHOICES = (
    ('private', 'This is private'),
    ('shared', 'This is shared'),
    ('public', 'This is public'),
)


class ImagrUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True, default='')
    USERNAME_FIELD = 'identifier'
    following = models.ManyToManyField("self", related_name='followers',
                                       verbose_name='People I follow',
                                       blank=True,
                                       null=True,
                                       symmetrical=False)

    date_joined = models.DateTimeField('date joined', default=timezone.now())


class Photo(models.Model):

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000, blank=True)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified', blank=True)
    date_published = models.DateTimeField('date published', blank=True)
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of photo",
                              related_name='photos')


class Album(models.Model):

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000, blank=True)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified', blank=True)
    date_published = models.DateTimeField('date published', blank=True)
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)
    owner = models.ForeignKey(ImagrUser, verbose_name="Owner of album")
    cover_photo = models.ForeignKey(Photo, related_name="cover_photo",
                                    blank=True)
    photos = models.ManyToManyField(Photo, verbose_name="photos in album",
                                    #limit_choices_to={'owner': owner},
                                    blank=True,
                                    )
