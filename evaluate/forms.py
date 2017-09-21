from evaluate.models import QuestionEvaluation
from django import forms


class EvalForm(forms.ModelForm):
    """ Form for evaluation of a question """

    q_num = forms.CharField(max_length=10, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(EvalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = QuestionEvaluation
        fields = ['evaluation', 'question']
        widgets = {'question': forms.HiddenInput()}


class BaseEvalFormSet(forms.BaseModelFormSet):
    """
    A base form set for sets of evaluation forms. Used to override built-in modelformset so that the EvalForm
    above can be used
    """
    def __init__(self, *args, **kwargs):
        super(BaseEvalFormSet, self).__init__(*args, **kwargs)
        self.form = EvalForm
