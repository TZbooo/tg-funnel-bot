# Generated by Django 4.1.4 on 2022-12-17 18:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0019_rename_phone_number_or_nickname_telegrambotclientmodel_phone_or_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambotclientmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата первого сообщения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegrambotclientmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего сообщения'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='chat_id',
            field=models.CharField(max_length=200, unique=True, verbose_name='ID telegram аккаунта'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='first_answer',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ответ на первый вопрос'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='free_rate',
            field=models.BooleanField(default=True, verbose_name='Бесплатный тариф'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='phone_or_nickname',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Телефон или ник юзера'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='second_answer',
            field=models.TextField(blank=True, max_length=4000, null=True, verbose_name='Ответ на второй вопрос'),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='third_answer',
            field=models.TextField(blank=True, max_length=4000, null=True, verbose_name='Ответ на третий вопрос'),
        ),
    ]