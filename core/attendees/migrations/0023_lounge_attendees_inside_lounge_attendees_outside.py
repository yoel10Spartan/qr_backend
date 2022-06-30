# Generated by Django 4.0.4 on 2022-06-12 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0022_alter_attendee_email_alter_attendee_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lounge',
            name='attendees_inside',
            field=models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_related_attendees_inside', to='attendees.attendee'),
        ),
        migrations.AddField(
            model_name='lounge',
            name='attendees_outside',
            field=models.ManyToManyField(blank=True, related_name='%(app_label)s_%(class)s_related_attendees_outside', to='attendees.attendee'),
        ),
    ]