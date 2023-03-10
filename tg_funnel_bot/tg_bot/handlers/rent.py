import uuid

from telebot.types import Message, CallbackQuery
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.conf import settings

from tg_funnel_bot.bot import bot
from tg_bot.models import BotMessagesSettingsModel
from tg_bot.utils import set_last_message_id
from tg_bot.keyboards.inline import only_back


def start_rent(message: Message):
    try:
        User = get_user_model()
        chat_id = message.chat.id
        admin_user = User.objects.filter(
            username__in=settings.ADMIN_USERS
        ).first()

        sended_message = bot.send_message(
            chat_id=chat_id,
            text='Создай свою воронку продаж',
            reply_markup=admin_user.get_start_rent_menu_markup()
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
    User = get_user_model()
    chat_id = query.from_user.id
    admin_user = User.objects.filter(
        username__in=settings.ADMIN_USERS
    ).first()

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text='Создай свою воронку продаж',
        reply_markup=admin_user.get_start_rent_menu_markup()
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
            reply_markup=only_back
        )
    except Exception as e:
        print(e)


def start_rent_new_bot(query: CallbackQuery):
    markup = BotMessagesSettingsModel.get_add_bot_message_markup()

    bot.edit_message_text(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        text='ссылка на страницу для создания нового бота',
        reply_markup=markup
    )


def get_bots_urls_menu(query: CallbackQuery):
    try:
        User = get_user_model()
        chat_id = query.from_user.id
        bots_onwer = User.objects.get(owner_chat_id=chat_id)

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text='ссылки на ваши боты-воронки, если тут ничего нет, значит, у вас еще нет ботов',
            reply_markup=bots_onwer.get_bots_urls_menu_message_markup()
        )
    except Exception as e:
        print(e)


def get_bots_change_menu(query: CallbackQuery):
    User = get_user_model()
    chat_id = query.from_user.id
    bots_onwer = User.objects.get(owner_chat_id=chat_id)

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=query.message.message_id,
        text='ссылки на страницы для изменения ваших ботов, если тут ничего нет, значит, у вас еще нет ботов',
        reply_markup=bots_onwer.get_change_bots_menu_message_markup()
    )


def pay_for_bot(query: CallbackQuery):
    try:
        User = get_user_model()
        chat_id = query.from_user.id
        bots_onwer = User.objects.get(owner_chat_id=chat_id)

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=query.message.message_id,
            text='оформите платную подписку на бота, чтобы убрать рекламное сообщение в начале диалога с ботом',
            reply_markup=bots_onwer.get_payment_link_menu()
        )
    except Exception as e:
        print(e)
