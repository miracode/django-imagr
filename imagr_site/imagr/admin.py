from django.contrib import admin
from imagr.models import Photo, Album, ImagrUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms
from django.core import urlresolvers


class AlbumAdmin(admin.ModelAdmin):

    readonly_fields = ['date_created', 'date_modified', 'date_published']

    list_display = ('title', 'linked_owner')

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

    def linked_owner(self, request):
        owner_url = urlresolvers.reverse('admin:imagr_imagruser_change',
                                         args=(request.owner.pk, ))
        user_name = request.owner.username
        string = '<a href="%s">%s</a>' % (owner_url, user_name)
        return string

    linked_owner.allow_tags = True



# This is taken directly from
# http://stackoverflow.com/questions/16953302/
# django-custom-user-model-in-admin-relation-auth-user-does-not-exist
# See discussion there on the weird django 'bug' it solves
class NewUserCreationForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            ImagrUser._default_manager.get(username=username)
        except ImagrUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = ImagrUser


class ImagrUserAdmin(UserAdmin):
    model = ImagrUser

    readonly_fields = ['followers_mask']
    add_form = NewUserCreationForm
    fieldsets = [item for item in UserAdmin.fieldsets] + [
        ('Followship', {'fields': ['following', 'followers_mask']}),
    ]

    list_display = ('username',)


class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ['date_uploaded', 'date_modified', 'date_published']

    list_display = ('title', 'linked_owner', 'file_size')
    list_filter = ['date_uploaded']
    search_fields = ['owner__username', 'owner__first_name',
                     'owner__last_name', 'owner__email']

    def linked_owner(self, request):
        owner_url = urlresolvers.reverse('admin:imagr_imagruser_change',
                                         args=(request.owner.pk, ))
        user_name = request.owner.username
        string = '<a href="%s">%s</a>' % (owner_url, user_name)
        return string

    linked_owner.allow_tags = True


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ImagrUser, ImagrUserAdmin)
