# Generated by Django 4.1.4 on 2022-12-19 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0028_rename_sent_message_count_telegrambotclientmodel_sent_messages_for_inactive_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_hour_message_text_second_part_inline_link',
        ),
        migrations.AddField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_day_message_text_first_part',
            field=models.TextField(default='Привет! Наверняка знаю, что вам будет интересен мануал как можно увеличить на 20% количество лидов без увеличения рекламного бюджета.', max_length=4000, verbose_name='Текст первого сообщения после 1 дня с последней активности пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_day_message_text_second_part',
            field=models.TextField(default='Все таки напомню, что я еще не получил ваши контактные данные. Если ваш интерес еще актуален, то укажите ниже ваш номер телефона или ник в телеграм:', max_length=4000, verbose_name='Текст второго сообщения после 1 дня с последней активности пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_two_days_message_text',
            field=models.TextField(default='Ну что ж это финальное сообщение. Больше не буду вам надоедать. Напомню, чтобы получить бесплатную и ничем не обязывающую консультацию по привлечению клиентов с помощью Facebook достаточно указать ваш номер телефона или ник в Телеграм:', max_length=4000, verbose_name='Текст сообщения после 2 дней с последней активности пользователя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_inline_button_link',
            field=models.URLField(default='https://youtube.com', verbose_name='Ссылка на кнопке второго сообщения после 1 часа с последней активности пользователя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_hour_message_text_first_part',
            field=models.TextField(max_length=4000, verbose_name='Текст первого сообщения после 1 часа с последней активности пользователя'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='user_inactive_for_hour_message_text_second_part',
            field=models.TextField(max_length=4000, verbose_name='Текст второго сообщения после 1 часа с последней активности пользователя'),
        ),
    ]
