import csv
import datetime
import json
import random
import string
from functools import reduce

import numpy as np
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

import management.forms as forms
import management.models as mdls
import management.slugger as slugify
from MembershipFunction import mf
from Stud_Eval import test
from evaluate.models import ExamEvaluation


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
def exam_change(request, exam_id):
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
        return redirect('manage:exam_change', exam_id=exam_id)

    if mfs:
        mfa = [{'eval_type': mf.get_eval_type_display(), 'membership_functions': mf.as_dicts()} for mf in mfs]
    else:
        mfa = [{'eval_type': val,
                'membership_functions': [{'num': 1, 'mf': [-0.1, 0.0, 0.1, 0.3]}, {'num': 2, 'mf': [0.1, 0.3, 0.5]},
                                         {'num': 3, 'mf': [0.3, 0.5, 0.7]},
                                         {'num': 4, 'mf': [0.5, 0.7, 0.9]}, {'num': 5, 'mf': [0.7, 0.9, 1.0, 1.1]}]}
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

    return render(request, 'management/change_exam.html', context)


def exam_manage(request, exam_id):
    exm = mdls.Exam.objects.get(pk=exam_id)
    qs = mdls.ExamQuestion.objects.filter(exam=exm).order_by('number')
    evals = ExamEvaluation.objects.filter(exam=exm)
    res = None

    context = {'exam': exm, 'evals': len(evals), 'num_qs': len(qs), 'questions': qs,
               'qs_sum': sum([q.teacher_eval for q in qs])}

    if request.POST.get('calc_eval'):
        res = gather_evaluation_results(exam_id)

    if request.POST.get('upload_data'):
        mfs = mdls.MembershipFunction.objects.filter(exam=exm).order_by('eval_type')
        context['sections'] = [{'eval_type': mf.get_eval_type_display(), 'membership_functions': mf.as_dicts()} for mf
                               in mfs]

    if request.POST.get('data'):
        data = json.loads(request.POST.get('data'))
        file = request.FILES.get('time-matrix')
        data['time'] = [[float(e) for e in line] for line in csv.reader(decode_utf8(file))]
        data['current_weights'] = [q.teacher_eval for q in qs]
        # print(data)
        res = calculate_evaluation_results(data)

    if res:
        new_weights = [{'number': i, 're_eval': v} for i, v in zip(range(1, len(res) + 1), res)]
        context['new_weights'] = new_weights
        context['new_weights_sum'] = sum([i['re_eval'] for i in new_weights])

    if request.POST.get('new_weights'):
        nw = [float(e) for e in request.POST.getlist('new_weights')]
        file = request.FILES.get('accuracy-matrix')
        accuracy = [[float(e) for e in line] for line in csv.reader(decode_utf8(file))]
        weights = [q.teacher_eval for q in qs]
        grades = []
        new_grades = []

        for l in accuracy:
            old_grade, new_grade = zip(*[(ow * a, nw * a) for ow, nw, a in zip(weights, nw, l)])
            old_grade = list(old_grade)
            new_grade = list(new_grade)
            new_grade.append(sum(new_grade))
            old_grade.append(sum(old_grade))
            new_grades.append(new_grade)
            grades.append(old_grade)

        context["new_weights"] = [{'number': i, 're_eval': w} for i, w in zip(range(1, len(nw) + 1), nw)]
        context["new_weights_sum"] = sum(nw)
        context["new_grades"] = new_grades
        context["old_grades"] = grades

    return render(request, 'management/manage_exam.html', context)


def decode_utf8(it):
    """ Decode a file in memory with utf-8 """
    for l in it:
        yield l.decode('utf-8')


def svg_test(request):
    return render(request, 'management/test.html')


def change_or_new(ms, ls, qs, exam):
    """
    Edit an existing MembershipFunction object or create new if it does not exist
    :param ms:
    :param ls:
    :param qs:
    :param exam:
    :return:
    """
    for c, et in mdls.MembershipFunction.EVAL_TYPES:
        change = False
        mf = str(ms[et]).replace("'", '"')
        labels = str(ls[et]).replace("'", '"')
        for q in qs:
            if q.get_eval_type_display() == et:
                q.mf = mf
                q.labels = labels
                q.save()
                change = True

        if not change:
            mdls.MembershipFunction(eval_type=c, mf=mf, labels=labels, exam=exam).save()


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


def calculate_evaluation_results(data):
    c = get_membership_degrees(data['qs']['Complexity'], data['mfs']['Complexity'])
    i = get_membership_degrees(data['qs']['Importance'], data['mfs']['Importance'])
    t = normalize_time(data['time'])
    g = data['current_weights']

    return test.run_evaluation(t.tolist(), c.tolist(), i.tolist(), g)


def gather_evaluation_results(exam_id):
    """
    Collect all evaluations of a given exam and send it to the matlab script
    :param exam_id: The exam id (pk)
    :return: List of new weights for each question
    """
    exam = mdls.Exam.objects.get(pk=exam_id)
    evals = ExamEvaluation.objects.filter(exam=exam)
    qs = mdls.ExamQuestion.objects.filter(exam=exam).order_by('number')
    w = [q.teacher_eval for q in qs]
    c = []
    i = []
    t = []
    c_mf = []
    i_mf = []

    for e in evals:
        cur_eval = e.get_evaluation()
        cur_mfs = e.get_mf()
        c_mf.append(cur_mfs['Complexity'])
        i_mf.append(cur_mfs['Importance'])
        c.append(cur_eval['Complexity'])  # get_membership_degrees(cur_eval['Complexity'], cur_mfs['Complexity']))
        i.append(cur_eval['Importance'])  # get_membership_degrees(cur_eval['Importance'], cur_mfs['Importance']))
        t.append(e.get_time())

    c = calc_mean(c)
    # print(c)
    i = calc_mean(i)
    t = normalize_time(t)
    c_mf = mat_calc_mean(c_mf)
    i_mf = mat_calc_mean(i_mf)

    rbs = test.compile_rulebases(
        {'Complexity': c_mf,  # [[0, 0, .1, .3], [.1, .3, .5], [.3, .5, .7], [.5, .7, .9], [.7, .9, 1, 1]],
         'Importance': i_mf})  # [[0, 0, .1, .3], [.1, .3, .5], [.3, .5, .7], [.5, .7, .9], [.7, .9, 1, 1]]})

    # print("Complexity:\n", c, "\nImportance:\n", i, "\nTime:\n", t)
    # print("Original weights:", g)
    # print("New weights", test.run_evaluation(t.tolist(), c.tolist(), i.tolist(), g))
    return test.evaluate(w, t, c, i, rbs)  # test.run_evaluation(t.tolist(), c.tolist(), i.tolist(), g)


def get_membership_degrees(crisp_set, mfs):
    """
    Calculate set of crisp values to a set of membership degrees
    :param crisp_set: Set of crisp values from which to make membership degrees
    :param mfs: Membership functions
    :return: Matrix (2D-array) of membership degrees
    """
    return np.array([[mf(x, cmf) for cmf in mfs] for x in crisp_set])


def calc_mean(lists):
    """
    Calculate element wise mean of a set of lists
    :param lists: Lists for which to calculate a list of mean elements
    :return: List of mean elements
    """
    num_eval = len(lists)
    avg = reduce(lambda a, b: a + b, lists)
    return [i/num_eval for i in avg]


def mat_calc_mean(mat_list):
    """
    Calculate the mean values (element wise) for a set of matrices
    :param mat_list: List of matrices from which to calculate a mean matrix
    :return: Matrix of mean values
    """
    num_eval = len(mat_list)
    avg = reduce(lambda a, b: [list_sum(i, j) for i, j in zip(a, b)], mat_list)
    return [[col / num_eval for col in row] for row in avg]


def list_sum(a, b):
    """
    Element wise sum of two lists
    E.g. [1, 2, 3] + [3, 5, 2] => [4, 7, 5]
    :param a: List a
    :param b: List b
    :return: Summed list
    """
    return [i + j for i, j in zip(a, b)]


def normalize_time(time_list):
    """
    Normalize a matrix of time values wrt largest time value for each question
    :param time_list: List of time values provided by student
    :return: Normalized matrix of time values
    """
    time = np.array(time_list)
    normalized = time / time.max(axis=0)

    return np.transpose(normalized)

#
# def calc_mean_mfs():
#
