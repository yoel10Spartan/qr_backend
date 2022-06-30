# Generated by Django 4.0.4 on 2022-06-10 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_aforo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='notice_consecutive_departures',
            new_name='count_trade_show_hours',
        ),
        migrations.RemoveField(
            model_name='event',
            name='notice_consecutive_entries',
        ),
        migrations.RemoveField(
            model_name='event',
            name='shares_account',
        ),
    ]