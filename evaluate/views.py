from django.shortcuts import render
from management.models import ExamQuestion, ExamEvaluationLink, MembershipFunction
from django.forms import modelformset_factory
import evaluate.forms as forms
import evaluate.models as mdls
import datetime
import re


def evaluate(request, url_hash):
    """ View for the evaluation of an exam """
    eval_link = ExamEvaluationLink.objects.get(url_hash=url_hash)

    if eval_link.expires < datetime.date.today():
        return render(request, 'evaluate/link_expired.html')

    exm_qs = ExamQuestion.objects.filter(exam=eval_link.exam).order_by('number')
    mfs = MembershipFunction.objects.filter(exam=eval_link.exam).order_by('eval_type')

    EvalFormSet = modelformset_factory(mdls.QuestionEvaluation, fields=('evaluation',), formset=forms.BaseEvalFormSet,
                                       extra=len(exm_qs))

    if request.POST:
        # fs = EvalFormSet(request.POST, queryset=mdls.QuestionEvaluation.objects.none())
        # if fs.is_valid():
        #     for form in fs:
        #         if form.is_valid():
        #             form.save()
        for key, val in request.POST.items():
            m = re.match(r'^(\d+)-(Complexity|Importance)$', key)
            if m:
                print("Match! Question", m.groups()[0], "on", m.groups()[1], "is", val)

    else:
        init_qs = [{'question': q.id, 'evaluation': None, 'q_num': q.number} for q in exm_qs]
        fs = EvalFormSet(initial=init_qs, queryset=mdls.QuestionEvaluation.objects.none())

    compl = ['Not at all', 'Fair', 'Quite', 'Very']

    if mfs:
        mfa = [{'eval_type': mf.get_eval_type_display(), 'membership_functions': mf.as_dicts(), 'opts': compl} for mf in mfs]
    else:
        mfa = [{'eval_type': val,
                'membership_functions': [{'num': 1, 'mf': [-1, 0, 1, 3]}, {'num': 2, 'mf': [1, 3, 5]},
                                         {'num': 3, 'mf': [3, 5, 7]},
                                         {'num': 4, 'mf': [5, 7, 9]}, {'num': 5, 'mf': [7, 9, 10, 11]}], 'opts': compl}
               for key, val in MembershipFunction.EVAL_TYPES]

    return render(request, 'evaluate/evaluate.html',
                  {'exam': eval_link.exam, 'questions': exm_qs, 'sections': mfa})
