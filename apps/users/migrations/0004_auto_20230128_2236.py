# Generated by Django 2.2.6 on 2023-01-28 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_self_introduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='self_introduction',
            field=models.TextField(blank=True, default='', max_length=300, null=True, verbose_name='自我介绍'),
        ),
    ]
