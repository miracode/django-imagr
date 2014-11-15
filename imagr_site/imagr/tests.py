from django.test import TestCase

from imagr.models import Album, Photo, ImagrUser

import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse


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


def create_user(username):
    """
    Create a user with only a username
    """
    return ImagrUser.objects.create(username=username)


def create_photo(title, description, days, owner):
    """
    Create a photo will number of days offset from now, + or -
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Photo.objects.create(title=title, description=description,
                                date_uploaded=time, date_published=time,
                                owner=owner)

# Not quite working
# class StreamViewTests(TestCase):
#     def test_stream_view_with_user_photos(self):
#         """
#         If no photos exists, stream should be empty
#         """
#         username = "Michelle"
#         create_user(username)
#         owner = ImagrUser.objects.filter(username=username)
#         create_photo('Cool Cat', 'cat with sunglasses', -2, owner[0])
#         response = self.client.get(reverse("imagr:stream"))
#         self.assertContains(response, 'Cool Cat')
