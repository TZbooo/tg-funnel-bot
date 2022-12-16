from telebot import TeleBot, types
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .models import BotMessagesSettingsModel, TelegramBotClientModel


bot = TeleBot(settings.TG_BOT_TOKEN)


class UpdatesHandlerBotAPIView(APIView):
    def post(self, request):
        json_data = request.body.decode('UTF-8')
        update_data = types.Update.de_json(json_data)
        bot.process_new_updates([update_data])

        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    start_message = bot_messages_settings.start_message
    bot.send_message(
        chat_id=message.chat.id,
        text=start_message,
        reply_markup=bot_messages_settings.get_start_message_markup()
    )
    TelegramBotClientModel.objects.get_or_create(
        chat_id=message.chat.id
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
    bot_client = TelegramBotClientModel.objects.get(chat_id=query.from_user.id)
    bot_client.first_answer = query.data.split('@')[1]
    bot_client.save()

    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    second_question_text = bot_messages_settings.second_question_text
    sended_message = bot.send_message(
        chat_id=query.from_user.id,
        text=second_question_text
    )
    bot.register_next_step_handler(
        message=sended_message,
        callback=second_question_input_message_handler
    )


def second_question_input_message_handler(message):
    bot_client = TelegramBotClientModel.objects.get(chat_id=message.chat.id)
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
    bot_messages_settings = BotMessagesSettingsModel.objects.all().first()
    after_loading_questions_data_text = bot_messages_settings.after_data_loading_text
    sended_message = bot.send_message(
        chat_id=message.chat.id,
        text=after_loading_questions_data_text
    )
    bot.register_next_step_handler(
        message=sended_message,
        callback=tg_nick_or_phone_number_input_handler
    )


def tg_nick_or_phone_number_input_handler(message):
    print(message.chat.id)
    bot_client = TelegramBotClientModel.objects.get(chat_id=message.chat.id)
    print(0)
    bot_client.phone_number_or_nickname = message.text
    bot_client.save()
    bot.send_message(
        chat_id=message.chat.id,
        text='ЗАЯВКА ОФОРМЛЕНА'
    )