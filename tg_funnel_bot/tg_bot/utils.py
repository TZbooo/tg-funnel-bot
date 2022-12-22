from telebot.types import Message, CallbackQuery

from .models import BotMessagesSettingsModel, TelegramBotClientModel


def get_bot_command_argument(command_message: Message, argument_number:int=1, default=None) -> str | None:
    try:
        return command_message.text.split()[argument_number]
    except IndexError:
        return default


def get_bot_query_argument(query: CallbackQuery, argument_number:int=0, default=None) -> str | None:
    try:
        return query.data.split('@')[1].split('_')[argument_number]
    except IndexError:
        return default


def register_new_bot_user(message: Message) -> BotMessagesSettingsModel:
    bot_username = get_bot_command_argument(message)
    bot_messages_settings = BotMessagesSettingsModel.objects.get(
        bot_username=bot_username
    )
    client, created = TelegramBotClientModel.objects.get_or_create(
        chat_id=message.chat.id,
    )
    client.bots.add(bot_messages_settings)
    client.save()
    return bot_messages_settings


def set_last_message_id(chat_id: str | int, sended_message: Message):
    client, created = TelegramBotClientModel.objects.get_or_create(
        chat_id=chat_id
    )
    client.last_message_id = sended_message.id
    client.save()