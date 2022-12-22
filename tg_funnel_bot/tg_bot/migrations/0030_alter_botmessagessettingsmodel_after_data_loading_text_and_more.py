# Generated by Django 4.1.4 on 2022-12-20 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tg_bot', '0029_remove_botmessagessettingsmodel_user_inactive_for_hour_message_text_second_part_inline_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='after_data_loading_text',
            field=models.TextField(max_length=4000, verbose_name='Текст сообщения после загрузки всех данных клиента'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='bot_username',
            field=models.CharField(max_length=200, unique=True, verbose_name='Имя бота'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='first_question_text',
            field=models.TextField(max_length=4000, verbose_name='Текст первого вопроса'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='start_message',
            field=models.TextField(max_length=4000, verbose_name='Текст сообщения после комманды /start'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='start_message_button_text',
            field=models.CharField(max_length=100, verbose_name='Текст на кнопке под сообщением от комманды /start'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='third_question_text',
            field=models.TextField(max_length=4000, verbose_name='Текст третьего вопроса'),
        ),
        migrations.AlterField(
            model_name='botmessagessettingsmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bots', to=settings.AUTH_USER_MODEL),
        ),
    ]