# Generated by Django 3.2.5 on 2021-07-31 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20210731_2009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='textbook',
            options={'ordering': ['-page']},
        ),
        migrations.AlterField(
            model_name='textbook',
            name='page',
            field=models.IntegerField(blank=True),
        ),
    ]
