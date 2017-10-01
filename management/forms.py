from management import models
from django import forms


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.Course
        fields = ['code']


class ExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.Exam
        fields = ['name']


class ExamQuestionForm(forms.ModelForm):
    """
    Modelform for Exam Questions
    """

    def __init__(self, *args, **kwargs):
        super(ExamQuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = models.ExamQuestion
        fields = ['teacher_eval', 'number']
        widgets = {'number': forms.HiddenInput()}


class BaseExamQuestionFormSet(forms.BaseModelFormSet):
    """
    A base form set for sets of exam question forms. Used to override built-in modelformset so that the ExamQuestionForm
    above can be used
    """
    def __init__(self, *args, **kwargs):
        super(BaseExamQuestionFormSet, self).__init__(*args, **kwargs)
        self.form = ExamQuestionForm

