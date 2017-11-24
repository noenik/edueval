from django.db import models
from django.contrib.auth.models import User
import datetime


class Course(models.Model):
    """ Model storing courses """
    code = models.CharField(max_length=10, unique=True)
    slug = models.CharField(max_length=10)
    description = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(User)


class Exam(models.Model):
    """ Model for exams beloging to a given course """
    name = models.CharField(max_length=75)
    course = models.ForeignKey(Course)


class ExamQuestion(models.Model):
    """ Model for questions belonging to a given exam """
    question = models.TextField(null=True)
    number = models.IntegerField()
    teacher_eval = models.IntegerField()
    exam = models.ForeignKey(Exam)


class ExamEvaluationLink(models.Model):
    """
    Model linking a url hash with an exam

    Valid for 3 days by default
    """
    url_hash = models.CharField(max_length=24, unique=True)
    expires = models.DateField(default=datetime.datetime.today() + datetime.timedelta(3))
    exam = models.ForeignKey(Exam)


class MembershipFunction(models.Model):
    EVAL_TYPES = (
        ('D', 'Difficulty'),
        ('C', 'Complexity'),
        ('I', 'Importance'),
    )

    x1 = models.FloatField()
    x2 = models.FloatField()
    x3 = models.FloatField()
    x4 = models.FloatField(null=True)
    mf = models.IntegerField()
    eval_type = models.CharField(max_length=1, choices=EVAL_TYPES)
    exam = models.ForeignKey(Exam)
