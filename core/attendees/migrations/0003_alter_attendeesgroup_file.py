# Generated by Django 4.0.4 on 2022-06-05 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_attendeesgroup_file_alter_attendee_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendeesgroup',
            name='file',
            field=models.FileField(upload_to='attendees_list'),
        ),
    ]