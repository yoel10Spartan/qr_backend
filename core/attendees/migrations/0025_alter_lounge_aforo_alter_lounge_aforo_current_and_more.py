# Generated by Django 4.0.4 on 2022-06-12 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0024_remove_lounge_attendees_inside_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lounge',
            name='aforo',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='lounge',
            name='aforo_current',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='lounge',
            name='afoto_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
