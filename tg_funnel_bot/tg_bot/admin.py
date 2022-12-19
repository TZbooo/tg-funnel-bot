from django.contrib import admin

from . import models


@admin.register(models.BotMessagesSettingsModel)
class BotMessagesSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot_username')


@admin.register(models.TelegramBotClientModel)
class TelegramBotClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_or_nickname')
    readonly_fields = ('created_at', 'updated_at')