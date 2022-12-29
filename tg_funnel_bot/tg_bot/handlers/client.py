
from telebot.types import Message, CallbackQuery
from django.contrib.auth import get_user_model
from django.conf import settings

from tg_funnel_bot.bot import bot
from ..models import BotMessagesSettingsModel, TelegramBotClientModel
from ..utils import (
    get_bot_query_argument,
    register_new_bot_user,
    set_last_message_id
)


def start_funnel_dialog(message: Message):
    try:
        chat_id = message.chat.id
        bot_messages_settings = register_new_bot_user(message)
        admin_user = get_user_model().objects.filter(
            username__in=settings.ADMIN_USERS
        ).first()
        start_message = bot_messages_settings.start_message

        sended_message = bot.send_message(
            chat_id=chat_id,
            text=start_message,
            reply_markup=bot_messages_settings.get_start_message_markup()
        )
        if bot_messages_settings.user.is_free_rate:
            bot.send_message(
                chat_id=chat_id,
                text=admin_user.add_message
            )
        set_last_message_id(
            chat_id=chat_id,
            sended_message=sended_message
        )
    except Exception as e:
        print(e)


def first_question_handler(query: CallbackQuery):
    try:
        chat_id = query.from_user.id
        bot_username = get_bot_query_argument(query)
        bot_messages_settings = BotMessagesSettingsModel.objects.get(
            bot_username=bot_username
        )
        first_question_text = bot_messages_settings.first_question_text
        bot.edit_message_text(
            text=first_question_text,
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=query.message.message_id,
            reply_markup=bot_messages_settings.get_first_question_markup()
        )
    except Exception as e:
        print(e)


def second_question_handler(query: CallbackQuery):
    try:
        chat_id = query.from_user.id
        bot_username = get_bot_query_argument(query, 1)

        bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
        bot_client.first_answer = get_bot_query_argument(query)
        bot_client.bot_wait_input_username = bot_username
        bot_client.save()

        bot_messages_settings = BotMessagesSettingsModel.objects.get(
            bot_username=bot_username
        )
        second_question_text = bot_messages_settings.second_question_text
        bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id
        )
        sended_message = bot.send_message(
            chat_id=chat_id,
            text=second_question_text
        )
        set_last_message_id(
            chat_id=chat_id,
            sended_message=sended_message
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=chat_id,
            callback=second_question_input_message_handler
        )
    except Exception as e:
        raise e


def second_question_input_message_handler(message: Message):
    try:
        chat_id = message.chat.id
        bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
        bot_client.second_answer = message.text
        bot_client.save()
        third_question_handler(message)
    except Exception as e:
        raise e


def third_question_handler(message: Message):
    try:
        chat_id = message.chat.id
        bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
        bot_messages_settings = BotMessagesSettingsModel.objects.get(
            bot_username=bot_client.bot_wait_input_username
        )
        third_question_text = bot_messages_settings.third_question_text
        bot.delete_message(
            chat_id=chat_id,
            message_id=message.id
        )
        bot.edit_message_text(
            text=third_question_text,
            chat_id=chat_id,
            message_id=bot_client.last_message_id
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=chat_id,
            callback=third_question_input_message_handler
        )
    except Exception as e:
        print(e)


def third_question_input_message_handler(message: Message):
    try:
        bot_client = TelegramBotClientModel.objects.get(chat_id=message.chat.id)
        bot_client.third_answer = message.text
        bot_client.save()
        after_loading_questions_data_handler(message)
    except Exception as e:
        print(e)


def after_loading_questions_data_handler(message: Message):
    try:
        chat_id = message.chat.id
        bot_client = TelegramBotClientModel.objects.get(chat_id=message.chat.id)
        
        bot_messages_settings = BotMessagesSettingsModel.objects.get(
            bot_username=bot_client.bot_wait_input_username
        )
        after_loading_questions_data_text = bot_messages_settings.after_data_loading_text
        bot.delete_message(
            chat_id=chat_id,
            message_id=message.id
        )
        bot.edit_message_text(
            text=after_loading_questions_data_text,
            chat_id=chat_id,
            message_id=bot_client.last_message_id
        )
        bot.register_next_step_handler_by_chat_id(
            chat_id=chat_id,
            callback=tg_nick_or_phone_input_handler
        )
    except Exception as e:
        print(e)


def tg_nick_or_phone_input_handler(message: Message):
    chat_id = message.chat.id
    bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
    bot_client.phone_or_nickname = message.text
    bot_client.save()

    bot.delete_message(
        chat_id=chat_id,
        message_id=message.id
    )
    bot.edit_message_text(
        text='ЗАЯВКА ОФОРМЛЕНА ✅',
        chat_id=chat_id,
        message_id=bot_client.last_message_id
    )

    bot.send_message(
        chat_id=chat_id,
        text='Вы все сделали верно. Ваши данные получены. Я свяжусь с вами в ближайшее время'
    )