# Generated by Django 4.1.4 on 2022-12-17 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0020_telegrambotclientmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='botmessagessettingsmodel',
            name='bot_username',
            field=models.CharField(default='omg', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]