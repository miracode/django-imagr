from django.test import TestCase

from imagr.models import Album, Photo, ImagrUser

import datetime
from django.utils import timezone


class PhotoMethodTests(TestCase):

    def test_was_published_recently_with_future_photo(self):
        """
        should return false if pub date is in future
        """
        time = timezone.now() + datetime.timedelta(days=5)
        future_photo = Photo(date_published=time)
        self.assertEqual(future_photo.was_published_recently(), False)

    def test_was_published_recently_with_old_photo(self):
        """
        should return false if pub date is more than 5 days old
        """
        time = timezone.now() - datetime.timedelta(days=6)
        old_photo = Photo(date_published=time)
        self.assertEqual(old_photo.was_published_recently(), False)
