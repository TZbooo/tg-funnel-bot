from telebot import TeleBot, types
from django.conf import settings

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)
bot.set_my_commands([
    types.BotCommand('/start', 'start'),
])