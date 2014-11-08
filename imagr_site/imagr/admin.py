from django.contrib import admin
from imagr.models import Photo, Album, ImagrUser


class AlbumAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        request.obj = obj
        return super(AlbumAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'photos':
            if request.obj is not None:
                kwargs['queryset'] = request.obj.owner.photos.all()
            else:
                # return no photos
                kwargs['queryset'] = Photo.objects.none()
        return super(AlbumAdmin, self).formfield_for_manytomany(db_field,
                                                                request,
                                                                **kwargs)


class ImagrUserAdmin(admin.ModelAdmin):

    fields = ['username', 'password', 'following',
              'date_joined']

admin.site.register(Photo)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ImagrUser, ImagrUserAdmin)
