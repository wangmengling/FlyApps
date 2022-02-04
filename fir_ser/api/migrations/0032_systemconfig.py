# Generated by Django 3.2.3 on 2022-02-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0031_auto_20220204_0906'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=256, unique=True, verbose_name='配置名称')),
                ('value', models.CharField(max_length=512, verbose_name='配置值')),
                ('description', models.CharField(blank=True, default='', max_length=256, verbose_name='备注')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '系统配置项',
                'verbose_name_plural': '系统配置项',
            },
        ),
    ]
