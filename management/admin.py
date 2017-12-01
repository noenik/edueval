from django.contrib import admin
from .models import Course, Exam, ExamQuestion, ExamEvaluationLink, MembershipFunction

admin.site.register((Course, Exam, ExamQuestion, ExamEvaluationLink, MembershipFunction))
