from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import management.forms as forms
import management.models as mdls


@login_required
def mng_home(request, course=None):
    courses = mdls.Course.objects.all()

    if request.POST:
        course_form = forms.CourseForm(request.POST or None)
        if course_form.is_valid():
            new_course = course_form.save(commit=False)
            new_course.owner = request.user
            new_course.save()
    else:
        course_form = forms.CourseForm()

    context = {'courses': courses, 'courseform': course_form}

    if course:
        context['selected_course'] = course
        context['exams'] = mdls.Exam.objects.filter(course__code=course)

    return render(request, 'management/mng_home.html', context)

