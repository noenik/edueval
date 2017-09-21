import random
import string

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render
import management.forms as forms
import management.models as mdls
import management.slugger as slugify
import datetime


@login_required
def mng_home(request, course=None):
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
    exm = mdls.Exam.objects.get(pk=exam_id)
    qs = mdls.ExamQuestion.objects.filter(exam=exm).order_by('number')

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
                                                formset=forms.BaseExamQuestionFormSet, extra=add_qs)
    context = {'exam': exm, 'questions': qs}

    if request.POST.get('save_qs'):
        fs = QuestionModelFormSet(request.POST, queryset=qs)
        context['qs_mdlformset'] = fs
        if fs.is_valid():
            for form in fs:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.exam = exm
                    instance.save()
    else:
        context['qs_mdlformset'] = QuestionModelFormSet(queryset=qs)

    if request.POST.get('get_link'):
        active_link = mdls.ExamEvaluationLink.objects.filter(exam=exm, expires__gte=datetime.datetime.today()).last()
        if active_link:
            print(active_link.url_hash)
            context['url_link'] = active_link
        else:
            context['url_link'] = generate_link(exm)

    return render(request, 'management/exam.html', context)


def generate_link(exm, exp=None):
    url_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
    el = mdls.ExamEvaluationLink(url_hash=url_hash, exam=exm)

    if exp:
        el.expires = exp

    obj = el.save()

    return obj
