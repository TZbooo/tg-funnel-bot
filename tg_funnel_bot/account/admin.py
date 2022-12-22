from django.contrib import admin
from django.contrib.auth.models import Group

from tg_bot.admin import PermissionsOnlyForAdminUsername
from . import models


admin.site.unregister(Group)


@admin.register(models.CustomUser)
class CustomUserAdmin(PermissionsOnlyForAdminUsername, admin.ModelAdmin):
    ...