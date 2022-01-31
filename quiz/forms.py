from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, modelformset_factory
from django.forms import ModelForm

from quiz.models import Choice


class ChoicesInlineFormset(BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)

        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        # num_correct_answers = sum(lst)

        if num_correct_answers == 0:
            raise ValidationError('Необходимо выбрать как минимум 1 вариант.')

        if num_correct_answers == len(self.forms):
            raise ValidationError('Не разрешено выбирать все варианты.')


class QuestionInlineFormset(BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Кол-во вопросов должно быть в диапазоне от {self.instance.QUESTION_MIN_LIMIT} '
                f'до {self.instance.QUESTION_MAX_LIMIT} включительно'
            )


class ChoiceForm(ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text', ]


ChoicesFormSet = modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
