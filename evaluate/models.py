from django.db import models
from management.models import ExamQuestion


class QuestionEvaluation(models.Model):
    """ Model that stores a student evaluation of a question """
    evaluation = models.IntegerField()
    question = models.ForeignKey(ExamQuestion)
