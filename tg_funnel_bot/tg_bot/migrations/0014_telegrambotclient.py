# Generated by Django 4.1.4 on 2022-12-16 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0013_botmessagessettingsmodel_after_data_loading_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBotClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=200, unique=True)),
                ('phone_number_or_nickname', models.CharField(max_length=200)),
                ('first_answer', models.CharField(max_length=200)),
                ('second_answer', models.TextField(max_length=4000)),
                ('third_answer', models.TextField(max_length=4000)),
            ],
        ),
    ]
