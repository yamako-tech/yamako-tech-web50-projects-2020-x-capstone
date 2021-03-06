# Generated by Django 3.2.5 on 2021-08-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_remove_lesson_student_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_eng', models.CharField(default='', max_length=10)),
                ('word_jap', models.CharField(default='', max_length=10)),
            ],
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['-created', '-updated']},
        ),
    ]
