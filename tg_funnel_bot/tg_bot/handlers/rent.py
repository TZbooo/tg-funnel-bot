import uuid

from telebot.types import Message, CallbackQuery
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.conf import settings

from tg_funnel_bot.bot import bot
from ..models import BotMessagesSettingsModel
from ..utils import set_last_message_id
from ..keyboards.inline import start_rent_markup, only_back


def start_rent(message: Message):
    try:
        chat_id = message.chat.id
        User = get_user_model()

        bot.delete_message(
            chat_id=chat_id,
            message_id=message.id
        )
        sended_message = bot.send_message(
            chat_id=chat_id,
            text='rent',
            reply_markup=start_rent_markup
        )
        password = get_random_string(length=20)
        if not User.objects.filter(
            owner_chat_id=chat_id
        ).exists():
            User.objects.create_superuser(
                username=uuid.uuid1(),
                password=password,
                owner_chat_id=chat_id,
                unhashed_password=password
            )
        set_last_message_id(
            chat_id=chat_id,
            sended_message=sended_message
        )
    except Exception as e:
        print(e)


def back_to_rent_menu(query: CallbackQuery):
    chat_id = query.from_user.id
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text='rent'
    )
    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=start_rent_markup
    )


def get_account(query: CallbackQuery):
    try:
        User = get_user_model()
        chat_id = query.from_user.id
        bot_owner_account = User.objects.get(owner_chat_id=chat_id)
        rate_information = 'бесплатный аккаунт'
        if not bot_owner_account.is_free_rate:
            rate_information = 'платная подписка'

        text = (f'username: {bot_owner_account.username}\n'
                f'password: {bot_owner_account.unhashed_password}\n'
                f'url: {settings.HOST_BASE_URL}/admin/\n'
                f'{rate_information}')
        bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=query.message.message_id,
        )
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=query.message.message_id,
            reply_markup=only_back
        )
    except Exception as e:
        print(e)


def start_rent_new_bot(query: CallbackQuery):
    markup = BotMessagesSettingsModel.get_add_bot_message_markup()

    bot.edit_message_reply_markup(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=markup
    )


def get_bots_urls_menu(query: CallbackQuery):
    try:
        User = get_user_model()
        chat_id = query.from_user.id
        bots_onwer = User.objects.get(owner_chat_id=chat_id)

        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=query.message.message_id,
            reply_markup=bots_onwer.get_bots_urls_menu_message_markup()
        )
    except Exception as e:
        print(e)


def get_bots_change_menu(query: CallbackQuery):
    User = get_user_model()
    chat_id = query.from_user.id
    bots_onwer = User.objects.get(owner_chat_id=chat_id)

    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=bots_onwer.get_change_bots_menu_message_markup()
    )


def pay_for_bot(query: CallbackQuery):
    User = get_user_model()
    chat_id = query.from_user.id
    bots_onwer = User.objects.get(owner_chat_id=chat_id)
    
    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=query.message.message_id,
        reply_markup=bots_onwer.get_payment_link_menu()
    )
