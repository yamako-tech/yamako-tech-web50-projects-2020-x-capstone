# Generated by Django 3.2.5 on 2021-08-01 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_auto_20210801_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='textbook',
            options={'ordering': ['title']},
        ),
        migrations.RemoveField(
            model_name='textbook',
            name='the_order',
        ),
    ]
