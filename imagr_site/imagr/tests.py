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
