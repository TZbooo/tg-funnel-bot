# Generated by Django 4.1.4 on 2022-12-27 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_rename_free_rate_customuser_is_free_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='add_message',
            field=models.TextField(default='Создай бесплатно такой же бот на https://hermesbot.top/', max_length=4000),
            preserve_default=False,
        ),
    ]
