from django.contrib import admin
from imagr_user.models import RegistrationManager, RegistrationProfile
# Register your models here.

admin.register(RegistrationManager)
admin.register(RegistrationProfile)
