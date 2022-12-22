from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from . import models


class PermissionsOnlyForAdminUsername:
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


@admin.register(models.BotMessagesSettingsModel)
class BotMessagesSettingsAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('user', 'bot_username')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            user__username=request.user.username
        )


@admin.register(models.TelegramBotClientModel)
class TelegramBotClientAdmin(PermissionsOnlyForAdminUsername, admin.ModelAdmin):
    list_display = ('phone_or_nickname',)
    readonly_fields = ('created_at', 'updated_at')