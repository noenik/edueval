from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User)
