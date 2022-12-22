from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db import models
from django.urls import reverse
from django.conf import settings
from django_better_admin_arrayfield.models.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from account.models import CustomUser


class BotMessagesSettingsModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='bots'
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
        models.CharField(max_length=50),
        verbose_name=_('Список кнопок с вариантами ответов для первого вопроса')
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

    def get_my_bot_funnel_link(self) -> str:
        return f'{settings.TELEGRAM_BOT_URL}?start={self.bot_username}'

    def get_start_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text=self.start_message_button_text,
                callback_data=f'start@{self.bot_username}'
            )
        )
        return markup

    def get_first_question_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        for question in self.first_question_buttons_text:
            markup.add(
                InlineKeyboardButton(
                    text=question,
                    callback_data=f'first@{question}_{self.bot_username}'
                )
            )
        return markup

    def get_inactive_message_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                text='ПОЛУЧИТЬ МАТЕРИАЛ',
                url=self.user_inactive_inline_button_link
            )
        )
        return markup

    def get_admin_change_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return settings.HOST_BASE_URL + reverse('admin:%s_%s_change' % info, args=(self.pk,))

    @classmethod
    def get_add_bot_message_markup(cls):
        info = (cls._meta.app_label, cls._meta.model_name)
        add_bot_url = settings.HOST_BASE_URL + reverse('admin:%s_%s_add' % info)
        return InlineKeyboardMarkup(keyboard=[
            [
                InlineKeyboardButton(
                    text='добавить нового бота',
                    url=add_bot_url
                )
            ],
            [
                InlineKeyboardButton(
                    text='⬅️ назад',
                    callback_data='back_to_rent_menu'
                )
            ]
        ])

    def __str__(self):
        return f'имя бота {self.bot_username}, имя мастера {self.user.username}'


class TelegramBotClientModel(models.Model):
    bots = models.ManyToManyField(
        BotMessagesSettingsModel,
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
    bot_wait_input_username = models.CharField(
        _('Имя бота, который ждёт входные данные'),
        max_length=200,
        null=True,
        blank=True
    )
    last_message_id = models.CharField(
        _('ID последнего сообщения'),
        max_length=200,
        unique=True,
        null=True,
        blank=True
    )

    free_rate = models.BooleanField(
        _('Бесплатный тариф'),
        default=True
    )
    sent_messages_for_inactive_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.phone_or_nickname}'