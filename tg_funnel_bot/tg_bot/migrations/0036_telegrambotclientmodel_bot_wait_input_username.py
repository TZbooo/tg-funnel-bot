# Generated by Django 4.1.4 on 2022-12-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0035_remove_telegrambotclientmodel_bot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegrambotclientmodel',
            name='bot_wait_input_username',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Имя бота'),
        ),
    ]
