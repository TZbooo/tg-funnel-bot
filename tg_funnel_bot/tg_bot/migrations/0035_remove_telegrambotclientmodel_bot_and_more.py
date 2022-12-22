# Generated by Django 4.1.4 on 2022-12-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0034_remove_telegrambotclientmodel_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrambotclientmodel',
            name='bot',
        ),
        migrations.AddField(
            model_name='telegrambotclientmodel',
            name='bot',
            field=models.ManyToManyField(related_name='clients', to='tg_bot.botmessagessettingsmodel'),
        ),
    ]