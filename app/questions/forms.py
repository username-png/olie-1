from django import forms

from model.tooling import predict

from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('text', 'tag',)
        widgets = {
            'tag': forms.RadioSelect(),
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 4}),
        }
