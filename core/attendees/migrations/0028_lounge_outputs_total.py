# Generated by Django 4.0.4 on 2022-06-20 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0027_remove_attendee_hour_remove_attendee_minut_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lounge',
            name='outputs_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
