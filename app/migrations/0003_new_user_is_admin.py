# Generated by Django 3.1.4 on 2021-01-30 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210131_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
