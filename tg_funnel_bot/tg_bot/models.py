from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


class TelegramBotClientModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='clients'
    )
    chat_id = models.CharField(
        _('ID telegram аккаунта'),
        max_length=200,
        unique=True
    )
    phone_or_nickname = models.CharField(
        _('Телефон или ник юзера'),
        max_length=200,
        null=True,
        blank=True
    )
    first_answer = models.CharField(
        _('Ответ на первый вопрос'),
        max_length=200,
        null=True,
        blank=True
    )
    second_answer = models.TextField(
        _('Ответ на второй вопрос'),
        max_length=4000,
        null=True,
        blank=True
    )
    third_answer = models.TextField(
        _('Ответ на третий вопрос'),
        max_length=4000,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        _('Дата первого сообщения'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата последнего сообщения'),
        auto_now=True
    )

    free_rate = models.BooleanField(
        _('Бесплатный тариф'),
        default=True
    )
    sent_messages_for_inactive_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} {self.phone_or_nickname}'


class BotMessagesSettingsModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='settings'
    )
    bot_username = models.CharField(
        _('Имя бота'),
        max_length=200,
        unique=True
    )
    start_message = models.TextField(
        _('Текст сообщения после комманды /start'),
        max_length=4000
    )
    start_message_button_text = models.CharField(
        _('Текст на кнопке под сообщением от комманды /start'),
        max_length=100
    )

    first_question_text = models.TextField(
        _('Текст первого вопроса'),
        max_length=4000
    )
    first_question_buttons_text = ArrayField(
        models.CharField(max_length=50)
    )
    second_question_text = models.TextField(max_length=4000)
    third_question_text = models.TextField(
        _('Текст третьего вопроса'),
        max_length=4000
    )
    after_data_loading_text = models.TextField(
        _('Текст сообщения после загрузки всех данных клиента'),
        max_length=4000
    )

    user_inactive_for_hour_message_text_first_part = models.TextField(
        _('Текст первого сообщения после 1 часа с последней активности пользователя'),
        max_length=4000
    )
    user_inactive_for_hour_message_text_second_part = models.TextField(
        _('Текст второго сообщения после 1 часа с последней активности пользователя'),
        max_length=4000
    )
    user_inactive_inline_button_link = models.URLField(
        _('Ссылка на кнопке второго сообщения после 1 часа с последней активности пользователя'),
        max_length=200
    )

    user_inactive_for_day_message_text_first_part = models.TextField(
        _('Текст первого сообщения после 1 дня с последней активности пользователя'),
        max_length=4000
    )
    user_inactive_for_day_message_text_second_part = models.TextField(
        _('Текст второго сообщения после 1 дня с последней активности пользователя'),
        max_length=4000
    )

    user_inactive_for_two_days_message_text = models.TextField(
        _('Текст сообщения после 2 дней с последней активности пользователя'),
        max_length=4000
    )

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

    def get_inactive_message_markup(self):
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text='ПОЛУЧИТЬ МАТЕРИАЛ',
                url=self.user_inactive_inline_button_link
            )
        )
        return markup

    def __str__(self):
        return f'имя бота {self.bot_username}, имя мастера {self.user.username}'