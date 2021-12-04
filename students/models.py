from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from adminsortable.models import SortableMixin
from django_pandas.managers import DataFrameManager


class User(AbstractUser):
    pass


class Course(models.Model):
    course_name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
	    return self.course_name


class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="lesson", null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lesson_teacher", null=True, blank=True)
    textbook = models.CharField(max_length=50, default="")
    page = models.IntegerField(null=True, blank=True, default="0", )
    score = models.IntegerField(verbose_name='score', blank=True, null=True, default=0,
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(15)])
    comment = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=False, null=False)
    updated = models.DateTimeField(auto_now=True, editable=False, blank=False, null=False)
    completed = models.BooleanField(default=False)
    objects = DataFrameManager()

    def __str__(self):
         return f"{self.student},{self.course},{self.textbook},{self.teacher}"

    class Meta:
        ordering = ['-created', '-updated']


class Word(models.Model):
    word_eng = models.CharField(max_length=10, default="")
    word_jap = models.CharField(max_length=10, default="")

    def __str__(self):
        return f"{self.word_eng},{self.word_jap}"


class MyWord(models.Model):
    student = models.ForeignKey(User, on_delete=models.PROTECT)
    new_word = models.CharField(max_length=20)
    meaning = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student}, {self.new_word}, {self.meaning}"



