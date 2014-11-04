import datetime

from django.db import models
from django.utils import timezone

PUBLISHED_CHOICES = (
    ('private', 'This is private'),
    ('shared', 'This is shared'),
    ('public', 'This is public'),
)


class Photo(models.Model):
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=2000)
    date_uploaded = models.DateTimeField('date uploaded')
    date_modified = models.DateTimeField('date modified')
    date_published = models.DateTimeField('date published')
    published = models.CharField(max_length=8, choices=PUBLISHED_CHOICES)


class Album(models.Model):
    pass