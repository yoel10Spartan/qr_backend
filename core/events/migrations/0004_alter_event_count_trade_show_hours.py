# Generated by Django 4.0.4 on 2022-06-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_rename_notice_consecutive_departures_event_count_trade_show_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='count_trade_show_hours',
            field=models.BooleanField(default=False),
        ),
    ]
