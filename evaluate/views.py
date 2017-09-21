from django.shortcuts import render
from management.models import ExamQuestion, ExamEvaluationLink
from django.forms import modelformset_factory
import evaluate.forms as forms
import evaluate.models as mdls
import datetime


def evaluate(request, url_hash):
    """ View for the evaluation of an exam """
    eval_link = ExamEvaluationLink.objects.get(url_hash=url_hash)

    if eval_link.expires < datetime.date.today():
        return render(request, 'evaluate/link_expired.html')

    exm_qs = ExamQuestion.objects.filter(exam=eval_link.exam).order_by('number')

    EvalFormSet = modelformset_factory(mdls.QuestionEvaluation, fields=('evaluation',), formset=forms.BaseEvalFormSet,
                                       extra=len(exm_qs))

    if request.POST:
        fs = EvalFormSet(request.POST, queryset=mdls.QuestionEvaluation.objects.none())
        if fs.is_valid():
            for form in fs:
                if form.is_valid():
                    form.save()
    else:
        init_qs = [{'question': q.id, 'evaluation': None, 'q_num': q.number} for q in exm_qs]
        fs = EvalFormSet(initial=init_qs, queryset=mdls.QuestionEvaluation.objects.none())

    return render(request, 'evaluate/evaluate.html', {'exam': eval_link.exam, 'questions': exm_qs, 'formset': fs})
