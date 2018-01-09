from django.shortcuts import render
from management.models import ExamQuestion, ExamEvaluationLink, MembershipFunction
import evaluate.models as mdls
import datetime
import re
import json


def evaluate(request, url_hash):
    """ View for the evaluation of an exam """
    eval_link = ExamEvaluationLink.objects.get(url_hash=url_hash)

    if eval_link.expires < datetime.date.today():
        return render(request, 'evaluate/link_expired.html')

    exm_qs = ExamQuestion.objects.filter(exam=eval_link.exam).order_by('number')
    mfs = MembershipFunction.objects.filter(exam=eval_link.exam).order_by('eval_type')

    if request.POST:
        time_rating = []
        eval_rating = {'Complexity': [], 'Importance': []}
        for key, val in request.POST.items():
            m = re.match(r'^(\d+)-(Complexity|Importance)$', key)
            if m:
                # print("Match! Question", m.groups()[0], "on", m.groups()[1], "is", val)
                eval_rating[m.groups()[1]].append(float(val))
            else:
                time = re.match(r'^(\d+)-time$', key)
                if time:
                    # print("Time rating on q", time.groups()[0], val)
                    time_rating.append(float(val))

        new_mfs = request.POST.get('mfs')

        new_eval = mdls.ExamEvaluation(
            evaluation=json.dumps(eval_rating),
            time=json.dumps(time_rating),
            membershipfunction=new_mfs,
            exam=eval_link.exam
        )

        new_eval.save()

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
