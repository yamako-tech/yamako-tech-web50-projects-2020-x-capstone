# Generated by Django 3.2.5 on 2021-08-01 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20210801_0825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='textbook',
            options={'ordering': ['the_order']},
        ),
        migrations.AddField(
            model_name='textbook',
            name='the_order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]