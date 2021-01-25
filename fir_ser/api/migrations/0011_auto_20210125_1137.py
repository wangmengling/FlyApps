# Generated by Django 3.0.3 on 2021-01-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_userinfo_api_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='udidsyncdeveloper',
            name='created_time',
        ),
        migrations.AddField(
            model_name='udidsyncdeveloper',
            name='platform',
            field=models.SmallIntegerField(choices=[(0, 'app developer'), (1, 'fly分发')], default=0, verbose_name='udid所在平台'),
        ),
    ]
