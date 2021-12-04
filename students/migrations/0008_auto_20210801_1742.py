# Generated by Django 3.2.5 on 2021-08-01 08:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20210801_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='score',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(15)], verbose_name=''),
        ),
    ]