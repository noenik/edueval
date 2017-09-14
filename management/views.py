from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.shortcuts import render
import management.forms as forms
import management.models as mdls
import urllib.parse as up
import management.slugger as slugify


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


def exam(request, exam_id):
    exm = mdls.Exam.objects.get(pk=exam_id)
    context = {'exam': exm}

    if request.POST:
        add_qs = request.POST.get('addQs')
        if add_qs:
            QuestionFormset = formset_factory(forms.ExamQuestionForm, extra=int(add_qs))
            formset = QuestionFormset()
            fs = [{'num': i, 'form': form} for i, form in zip(range(1, len(formset)+1), formset)]
            context['question_formset'] = fs
            context['management_form'] = formset.management_form
        else:
            QuestionFormset = formset_factory(forms.ExamQuestionForm)
            fs = QuestionFormset(request.POST)

            if fs.is_valid():
                fs.save()

    return render(request, 'management/exam.html', context)
