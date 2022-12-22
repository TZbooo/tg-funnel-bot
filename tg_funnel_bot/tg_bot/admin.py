from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from . import models


@admin.register(models.BotMessagesSettingsModel)
class BotMessagesSettingsAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('bot_username',)
    exclude = ('user',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            user__username=request.user.username
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)


@admin.register(models.TelegramBotClientModel)
class TelegramBotClientAdmin(admin.ModelAdmin):
    list_display = ('phone_or_nickname',)
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('bots',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            bots__user__username=request.user.username
        )