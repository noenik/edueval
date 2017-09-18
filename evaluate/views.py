from django.shortcuts import render
from management.models import Exam, ExamQuestion


def evaluate(request, id):
    """ View for the evaluation of an exam """
    exm = Exam.objects.get(pk=id)
    exm_qs = ExamQuestion.objects.filter(exam=exm)

    return render(request, 'evakuate/evaluate.html', {'exam': exm, 'questions': exm_qs})
