# Generated by Django 4.2 on 2023-04-21 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0011_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='showing',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
