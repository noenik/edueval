from evaluate.models import QuestionEvaluation
from django import forms


class EvalForm(forms.ModelForm):
    """ Form for evaluation of a question """

    question = forms.IntegerField()

    class Meta:
        model = QuestionEvaluation
        fields = ['evaluation']
