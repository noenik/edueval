import random
import string
import json

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render
import management.forms as forms
import management.models as mdls
import management.slugger as slugify
import datetime


@login_required
def mng_home(request, course=None):
    """
    View for management home page
    :param request:
    :param course:
    :return:
    """
    courses = mdls.Course.objects.all()
    course_form = forms.CourseForm(request.POST or None)
    context = {'courses': courses, 'courseform': course_form}

    if course:
        selected_course = mdls.Course.objects.get(slug=course)
        exam_form = forms.ExamForm(request.POST or None)
        context['selected_course'] = selected_course
        context['exams'] = mdls.Exam.objects.filter(course__slug=course)
        context['examform'] = exam_form

        if request.POST and exam_form.is_valid():
            new_exam = exam_form.save(commit=False)
            new_exam.course = selected_course
            new_exam.save()

    if request.POST:
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.owner = request.user
            new_course.slug = slugify.slug(new_course.code)
            new_course.save()

    return render(request, 'management/mng_home.html', context)


@login_required
def exam(request, exam_id):
    """
    View for a detailed page for an exam
    :param request:
    :param exam_id:
    :return:
    """
    exm = mdls.Exam.objects.get(pk=exam_id)
    qs = mdls.ExamQuestion.objects.filter(exam=exm).order_by('number')
    mfs = mdls.MembershipFunction.objects.filter(exam=exm).order_by('eval_type')

    add_qs = request.POST.get('addQs')
    initial = request.POST.get('form-INITIAL_FORMS')
    total = request.POST.get('form-TOTAL_FORMS')
    if add_qs:
        add_qs = int(add_qs)
        if initial and total:
            add_qs += int(total) - int(initial)
    elif initial and total:
        add_qs = int(total) - int(initial)
    else:
        add_qs = 0

    QuestionModelFormSet = modelformset_factory(mdls.ExamQuestion, fields=('teacher_eval',),
                                                formset=forms.BaseExamQuestionFormSet, extra=add_qs, can_delete=True)

    mss = request.POST.get('memberships')
    labels = request.POST.get('labels')
    if mss and labels:
        labels = json.loads(labels)
        memberships = json.loads(mss)
        change_or_new(memberships, labels, mfs, exm)

    if mfs:
        mfa = [{'eval_type': mf.get_eval_type_display(), 'membership_functions': mf.as_dicts()} for mf in mfs]
    else:
        mfa = [{'eval_type': val,
                'membership_functions': [{'num': 1, 'mf': [-1, 0, 1, 3]}, {'num': 2, 'mf': [1, 3, 5]},
                                         {'num': 3, 'mf': [3, 5, 7]},
                                         {'num': 4, 'mf': [5, 7, 9]}, {'num': 5, 'mf': [7, 9, 10, 11]}]}
               for key, val in mdls.MembershipFunction.EVAL_TYPES]

    context = {'exam': exm, 'questions': qs, 'mfa': mfa}

    if request.POST.get('save_qs'):
        fs = QuestionModelFormSet(request.POST, queryset=qs)
        context['qs_mdlformset'] = fs
        if fs.is_valid():
            for form in fs:
                if form.is_valid():
                    if form.cleaned_data.get('DELETE'):
                        form.cleaned_data.get('id').delete()
                    else:
                        instance = form.save(commit=False)
                        instance.exam = exm
                        instance.save()
            context['message'] = "Exam successfully saved"
    else:
        context['qs_mdlformset'] = QuestionModelFormSet(queryset=qs)

    if request.POST.get('get_link'):
        active_link = mdls.ExamEvaluationLink.objects.filter(exam=exm, expires__gte=datetime.datetime.today()).last()
        if active_link:
            context['url_link'] = active_link
        else:
            context['url_link'] = generate_link(exm)

    return render(request, 'management/exam.html', context)


def svg_test(request):
    return render(request, 'management/test.html')


def change_or_new(ms, ls, qs, exam):
    for c, et in mdls.MembershipFunction.EVAL_TYPES:
        change = False
        for q in qs:
            if q.get_eval_type_display() == et:
                q.mf = str(ms[et]).replace("'", '"')
                q.labels = str(ls[et]).replace("'", '"')
                q.save()
                change = True

        if not change:
            mdls.MembershipFunction(eval_type=c, mf=ms[et], labels=ls[et], exam=exam).save()


def generate_link(exm, exp=None):
    """
    Generate a url hash and link it to an exam. Creates a ExamEvaluationLink object that contains the hash,
    link to an exam, and and expiration date. By default the link expires 3 days after creation. Can be overridden
    by giving the exp argument.
    :param exm: Exam object to link a hash with
    :param exp: Expiration day
    :return: The ExamEvaluationLink object
    """
    url_hash = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    el = mdls.ExamEvaluationLink(url_hash=url_hash, exam=exm)

    if exp:
        el.expires = exp

    el.save()

    return el
