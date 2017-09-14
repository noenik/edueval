from .models import Course, Exam, ExamQuestion
from django import forms


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Course
        fields = ['code']


class ExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Exam
        fields = ['name']


class ExamQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamQuestionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ExamQuestion
        fields = ['teacher_eval']
