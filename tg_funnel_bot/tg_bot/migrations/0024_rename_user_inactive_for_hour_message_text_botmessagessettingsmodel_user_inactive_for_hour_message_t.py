# Generated by Django 4.1.4 on 2022-12-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0023_telegrambotclientmodel_request_sent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botmessagessettingsmodel',
            old_name='user_inactive_for_hour_message_text',
            new_name='user_inactive_for_hour_message_text_for_input',
        ),
        migrations.AddField(
            model_name='telegrambotclientmodel',
            name='message_for_on_hour_inactive_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='request_sent',
            field=models.BooleanField(default=False, verbose_name='Заявка успешно отправлена'),
        ),
    ]
