# Generated by Django 4.1.4 on 2022-12-16 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0006_rename_telegramusercondition_telegramuserconditionmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuserconditionmodel',
            old_name='current_condition',
            new_name='condition',
        ),
    ]