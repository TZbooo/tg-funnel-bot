# Generated by Django 4.1.4 on 2022-12-16 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0008_telegramuserconditionmodel_condition_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botquestionmodel',
            name='priority',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
