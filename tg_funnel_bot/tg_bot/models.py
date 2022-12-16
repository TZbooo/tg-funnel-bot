from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _


class TelegramBotClientModel(models.Model):
    chat_id = models.CharField(
        max_length=200,
        unique=True
    )
    phone_number_or_nickname = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    first_answer = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    second_answer = models.TextField(
        max_length=4000,
        null=True,
        blank=True
    )
    third_answer = models.TextField(
        max_length=4000,
        null=True,
        blank=True
    )


class BotMessagesSettingsModel(models.Model):
    start_message = models.TextField(max_length=4000)
    start_message_button_text = models.CharField(max_length=100)

    first_question_text = models.TextField(max_length=4000)
    first_question_buttons_text = ArrayField(
        models.CharField(max_length=50)
    )

    second_question_text = models.TextField(max_length=4000)

    third_question_text = models.TextField(max_length=4000)

    after_data_loading_text = models.TextField(max_length=4000)

    def get_start_message_markup(self):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                self.start_message_button_text,
                callback_data=f'start_interview'
            )
        )
        return markup

    def get_first_question_markup(self):
        markup = InlineKeyboardMarkup()
        for question in self.first_question_buttons_text:
            markup.add(
                InlineKeyboardButton(
                    question,
                    callback_data=f'firstquestion@{question}'
                )
            )
        return markup