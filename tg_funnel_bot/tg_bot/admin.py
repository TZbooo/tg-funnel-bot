from django.contrib import admin
from django.contrib.admin import filters
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from . import models


@admin.register(models.BotMessagesSettingsModel)
class BotMessagesSettingsAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('bot_username',)
    exclude = ('user',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(
            user__username=request.user.username
        )
        if request.user.username == 'admin':
            queryset = super().get_queryset(request)
        return queryset

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)


class BotsFilter(filters.SimpleListFilter):
    title = _('Бот с которым взаимодействовал клиент')
    parameter_name = 'bots'

    def lookups(self, request, model_admin):
        return ((bot.bot_username, bot.bot_username) for bot in request.user.bots.all())

    def queryset(self, request, queryset):
        if self.value() and request.user.username not in settings.ADMIN_USERS:
            return queryset.filter(bots__bot_username=self.value())
        return queryset


@admin.register(models.TelegramBotClientModel)
class TelegramBotClientAdmin(admin.ModelAdmin):
    list_display = ('phone_or_nickname',)
    list_filter = (BotsFilter,)
    exclude = ('bots',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(
            bots__user__username=request.user.username
        )
        if request.user.username == 'admin':
            queryset = super().get_queryset(request)
        return queryset