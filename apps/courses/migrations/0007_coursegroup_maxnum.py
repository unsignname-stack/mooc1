# Generated by Django 2.2.6 on 2023-02-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20230221_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursegroup',
            name='maxNum',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='小组人数上限'),
        ),
    ]
