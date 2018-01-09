from django.db import models
from django.contrib.auth.models import User
import datetime
import json


def get_date():
    return datetime.datetime.today() + datetime.timedelta(days=3)


class Course(models.Model):
    """ Model storing courses """
    code = models.CharField(max_length=10, unique=True)
    slug = models.CharField(max_length=10)
    description = models.CharField(max_length=200, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Exam(models.Model):
    """ Model for exams beloging to a given course """
    name = models.CharField(max_length=75)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class ExamQuestion(models.Model):
    """ Model for questions belonging to a given exam """
    question = models.TextField(null=True)
    number = models.IntegerField()
    teacher_eval = models.IntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)


class ExamEvaluationLink(models.Model):
    """
    Model linking a url hash with an exam

    Valid for 3 days by default
    """
    url_hash = models.CharField(max_length=24, unique=True)
    expires = models.DateField(default=get_date)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)


class MembershipFunction(models.Model):
    EMAP = {'Complexity': 'C', 'Importance': 'I'}
    EVAL_TYPES = (
        ('C', 'Complexity'),
        ('I', 'Importance'),
    )
    mf = models.CharField(max_length=150)
    labels = models.CharField(max_length=150, null=True)
    eval_type = models.CharField(max_length=1, choices=EVAL_TYPES)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def as_dicts(self):
        lst = json.loads(self.mf)
        if self.labels:
            labels = json.loads(self.labels)
        else:
            labels = ['']*len(lst)
        return [{'num': num, 'mf': mf, 'label': l} for num, mf, l in zip(range(1, len(lst)+1), lst, labels)]

