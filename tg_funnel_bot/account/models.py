from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class CustomUser(AbstractUser):
    owner_chat_id = models.CharField(
        _('ID telegram аккаунта ботовода'),
        max_length=200,
        unique=True
    )
    unhashed_password = models.CharField(
        max_length=20
    )

    def get_bots_urls_menu_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for bot in self.bots.all():
            markup.add(
                InlineKeyboardButton(
                    text=bot.bot_username,
                    url=bot.get_my_bot_funnel_link()
                )
            )
        markup.add(
            InlineKeyboardButton(
                text='⬅️ назад',
                callback_data='back_to_rent_menu'
            )
        )
        return markup

    def get_change_bots_menu_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for bot in self.bots.all():
            markup.add(
                InlineKeyboardButton(
                    text=bot.bot_username,
                    url=bot.get_admin_change_url()
                )
            )
        markup.add(
            InlineKeyboardButton(
                text='⬅️ назад',
                callback_data='back_to_rent_menu'
            )
        )
        return markup
