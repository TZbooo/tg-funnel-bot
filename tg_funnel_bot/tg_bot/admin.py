from django.contrib import admin

from . import models


@admin.register(models.BotMessagesSettingsModel)
class BotMessagesSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TelegramBotClientModel)
class TelegramBotClientAdmin(admin.ModelAdmin):
    pass