from typing import Self

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_funnel_bot.stripe import stripe


def end_with_back_to_rent_menu_inline_button(func):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs).add(
            InlineKeyboardButton(
                text='⬅️ назад',
                callback_data='back_to_rent_menu'
            )
        )
    return wrapped


class CustomUser(AbstractUser):
    owner_chat_id = models.CharField(
        _('ID telegram аккаунта ботовода'),
        max_length=200,
        unique=True
    )
    unhashed_password = models.CharField(
        max_length=20
    )
    is_free_rate = models.BooleanField(
        _('Бесплатный тариф'),
        default=True
    )
    add_message = models.TextField(max_length=4000)

    @end_with_back_to_rent_menu_inline_button
    def get_bots_urls_menu_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for bot in self.bots.all():
            markup.add(
                InlineKeyboardButton(
                    text=bot.bot_username,
                    url=bot.get_my_bot_funnel_link()
                )
            )
        return markup

    @end_with_back_to_rent_menu_inline_button
    def get_change_bots_menu_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for bot in self.bots.all():
            markup.add(
                InlineKeyboardButton(
                    text=bot.bot_username,
                    url=bot.get_admin_change_url()
                )
            )
        return markup

    def get_payment_link(self) -> str:
        payment_link = stripe.PaymentLink.create(
            line_items=[{
                'price': settings.STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            metadata={
                'bots_owner_id': self.owner_chat_id
            }
        )
        return payment_link.get('url')

    @end_with_back_to_rent_menu_inline_button
    def get_payment_link_menu(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(keyboard=[
            [
                InlineKeyboardButton(
                    text='оплатить',
                    url=self.get_payment_link()
                )
            ]
        ])

    def switch_to_paid_rate(self) -> Self:
        self.is_free_rate = False
        return self