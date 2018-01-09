from django.db import models
from management.models import Exam, MembershipFunction
import json


class ExamEvaluation(models.Model):
    """ Model that stores a student evaluation of an exam """
    evaluation = models.CharField(max_length=150)
    time = models.CharField(max_length=150)
    membershipfunction = models.CharField(max_length=150)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def get_evaluation(self):
        return json.loads(self.evaluation)

    def get_time(self):
        return json.loads(self.time)

    def get_mf(self):
        return json.loads(self.membershipfunction)
