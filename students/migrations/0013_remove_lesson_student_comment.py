# Generated by Django 3.2.5 on 2021-08-03 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_lesson_student_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='student_comment',
        ),
    ]