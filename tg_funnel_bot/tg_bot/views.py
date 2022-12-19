import django.utils.timezone as tz
from telebot import types
from rest_framework.views import APIView
from rest_framework.response import Response
from celery import shared_task

from tg_funnel_bot.bot import bot
from .models import BotMessagesSettingsModel, TelegramBotClientModel


class UpdatesHandlerBotAPIView(APIView):
    def post(self, request):
        json_data = request.body.decode('UTF-8')
        update_data = types.Update.de_json(json_data)
        bot.process_new_updates([update_data])

        no_nick_or_phone_clients = TelegramBotClientModel.objects.filter(
            chat_id=update_data.message.chat.id,
            phone_or_nickname=None
        ).exclude(
            sent_messages_for_inactive_count=0
        )
        if no_nick_or_phone_clients.exists():
            no_nick_or_phone_clients.update(sent_messages_for_inactive_count=0)
            tg_nick_or_phone_input_handler(update_data.message)

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    start_message = bot_messages_settings.start_message
    chat_id = message.chat.id
    bot.send_message(
        chat_id=chat_id,
        text=start_message,
        reply_markup=bot_messages_settings.get_start_message_markup()
    )
    TelegramBotClientModel.objects.get_or_create(
        chat_id=chat_id
    )


@bot.callback_query_handler(lambda query: query.data == 'start_interview')
def first_question_handler(query):
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    first_question_text = bot_messages_settings.first_question_text
    bot.send_message(
        chat_id=query.from_user.id,
        text=first_question_text,
        reply_markup=bot_messages_settings.get_first_question_markup()
    )


@bot.callback_query_handler(lambda query: 'firstquestion@' in query.data)
def second_question_handler(query):
    chat_id = query.from_user.id
    bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
    bot_client.first_answer = query.data.split('@')[1]
    bot_client.save()

    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    second_question_text = bot_messages_settings.second_question_text
    bot.send_message(
        chat_id=chat_id,
        text=second_question_text
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=chat_id,
        callback=second_question_input_message_handler
    )


def second_question_input_message_handler(message):
    chat_id = message.chat.id
    bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
    bot_client.second_answer = message.text
    bot_client.save()
    third_question_handler(message)

def third_question_handler(message):
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    third_question_text = bot_messages_settings.third_question_text
    sended_message = bot.send_message(
        chat_id=message.chat.id,
        text=third_question_text
    )
    bot.register_next_step_handler(
        message=sended_message,
        callback=third_question_input_message_handler
    )


def third_question_input_message_handler(message):
    bot_client = TelegramBotClientModel.objects.get(chat_id=message.chat.id)
    bot_client.third_answer = message.text
    bot_client.save()
    after_loading_questions_data_handler(message)


def after_loading_questions_data_handler(message):
    chat_id = message.chat.id
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    after_loading_questions_data_text = bot_messages_settings.after_data_loading_text
    bot.send_message(
        chat_id=chat_id,
        text=after_loading_questions_data_text
    )
    bot.register_next_step_handler_by_chat_id(
        chat_id=chat_id,
        callback=tg_nick_or_phone_input_handler
    )


def tg_nick_or_phone_input_handler(message):
    chat_id = message.chat.id
    bot_client = TelegramBotClientModel.objects.get(chat_id=chat_id)
    bot_client.phone_or_nickname = message.text
    bot_client.save()

    bot.send_message(
        chat_id=chat_id,
        text='ЗАЯВКА ОФОРМЛЕНА'
    )
    bot.send_message(
        chat_id=chat_id,
        text='Вы все сделали верно. Ваши данные получены. Я свяжусь с вами в ближайшее время'
    )


@shared_task(name='send_certain_messages_for_inactive_users')
def send_certain_messages_for_inactive_users():
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()

    no_nick_or_phone_clients = TelegramBotClientModel.objects.filter(
        phone_or_nickname=None
    )
    inactive_for_two_days_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=5),
        sent_messages_for_inactive_count=2
    )
    inactive_for_day_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=3),
        sent_messages_for_inactive_count=1
    ).difference(inactive_for_two_days_clients)
    inactive_for_hour_clients = no_nick_or_phone_clients.filter(
        updated_at__lte=tz.now() - tz.timedelta(minutes=2),
        sent_messages_for_inactive_count=0
    ).difference(inactive_for_day_clients)

    for inactive_client in inactive_for_hour_clients:
        chat_id = inactive_client.chat_id
        bot.send_message(
            chat_id=chat_id,
            text=bot_messages_settings.user_inactive_for_hour_message_text_first_part
        )
        bot.send_message(
            chat_id=chat_id,
            text=bot_messages_settings.user_inactive_for_hour_message_text_second_part,
            reply_markup=bot_messages_settings.get_inactive_message_markup()
        )
        inactive_client.sent_messages_for_inactive_count += 1
        inactive_client.save()

    for inactive_client in inactive_for_day_clients:
        chat_id = inactive_client.chat_id
        bot.send_message(
            chat_id=chat_id,
            text=bot_messages_settings.user_inactive_for_day_message_text_first_part,
            reply_markup=bot_messages_settings.get_inactive_message_markup()
        )
        bot.send_message(
            chat_id=chat_id,
            text=bot_messages_settings.user_inactive_for_day_message_text_second_part
        )
        inactive_client.sent_messages_for_inactive_count += 1
        inactive_client.save()

    for inactive_client in inactive_for_two_days_clients:
        chat_id = inactive_client.chat_id
        bot.send_message(
            chat_id=chat_id,
            text=bot_messages_settings.user_inactive_for_two_days_message_text
        )
        inactive_client.sent_messages_for_inactive_count += 1
        inactive_client.save()
    return tz.now()