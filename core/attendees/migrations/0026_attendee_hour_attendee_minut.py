# Generated by Django 4.0.4 on 2022-06-20 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0025_alter_lounge_aforo_alter_lounge_aforo_current_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='attendee',
            name='minut',
            field=models.IntegerField(default=0),
        ),
    ]
