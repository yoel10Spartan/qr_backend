# Generated by Django 4.0.4 on 2022-06-07 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0011_alter_attendee_hours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='attendees_group',
        ),
    ]
