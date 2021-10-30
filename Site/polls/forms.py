from django.forms import ModelForm, TextInput
from .models import Question, Choice


class CreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']

        widgets = {
            "question_text": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вопрос'
            }),
        }

class CreateChoice(ModelForm):
     class Meta:
        model = Choice
        fields = ['choice_text', 'question']

        widgets = {
            "choice_text": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вопрос'
            }),
        }