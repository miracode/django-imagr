from django.contrib import admin
from imagr.models import Photo, Album, ImagrUser

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(ImagrUser)