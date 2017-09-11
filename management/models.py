from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    slug = models.CharField(max_length=10)
    description = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(User)


class Exam(models.Model):
    name = models.CharField(max_length=75)
    course = models.ForeignKey(Course)


class ExamQuestion(models.Model):
    question = models.TextField(null=True)
    teacher_eval = models.IntegerField()
    exam = models.ForeignKey(Exam)
