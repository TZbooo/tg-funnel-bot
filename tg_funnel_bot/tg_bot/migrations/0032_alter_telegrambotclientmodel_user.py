# Generated by Django 4.1.4 on 2022-12-20 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0031_alter_telegrambotclientmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambotclientmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bots', to='tg_bot.botmessagessettingsmodel'),
        ),
    ]
