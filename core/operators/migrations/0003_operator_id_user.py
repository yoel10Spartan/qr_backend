# Generated by Django 4.0.4 on 2022-06-18 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operators', '0002_remove_operator_lounge'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='id_user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
