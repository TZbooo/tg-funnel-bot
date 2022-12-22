from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


admin.site.unregister(Group)


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return True if request.user.username == 'admin' else False

    def has_add_permission(self, request):
        return True if request.user.username == 'admin' else False

    def has_change_permission(self, request, *args, **kwargs):
        return True if request.user.username == 'admin' else False

    def has_delete_permission(self, request, *args, **kwargs):
        return True if request.user.username == 'admin' else False

    def has_view_permission(self, request, *args, **kwargs):
        return True if request.user.username == 'admin' else False