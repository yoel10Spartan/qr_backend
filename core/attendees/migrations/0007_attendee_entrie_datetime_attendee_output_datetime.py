# Generated by Django 4.0.4 on 2022-06-06 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0006_lounge_aforo_lounge_aforo_current'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='entrie_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='output_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
