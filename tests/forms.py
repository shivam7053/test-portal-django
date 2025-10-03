from django import forms
from .models import Test, Question, Choice
from django.forms import inlineformset_factory

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'text', 'question_type']
        widgets = {
            'text': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
            'question_type': forms.Select(attrs={'class':'form-select'}),
            'test': forms.Select(attrs={'class':'form-select'}),
        }

ChoiceFormSet = inlineformset_factory(
    Question, Choice,
    fields=('text','is_correct'),
    extra=4,
    widgets={
        'text': forms.TextInput(attrs={'class':'form-control'}),
        'is_correct': forms.CheckboxInput(attrs={'class':'form-check-input'})
    }
)
