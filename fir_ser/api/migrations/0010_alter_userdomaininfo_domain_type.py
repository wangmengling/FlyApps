# Generated by Django 3.2.3 on 2021-09-23 12:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0009_userdomaininfo_domain_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdomaininfo',
            name='domain_type',
            field=models.SmallIntegerField(choices=[(0, '下载码域名'), (1, '下载页域名'), (2, '应用专用域名')], default=1,
                                           help_text='0 表示下载码域名，扫描下载码域名，会自动跳转到预览域名', verbose_name='域名类型'),
        ),
    ]
