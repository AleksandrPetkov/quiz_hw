from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Questions count must be range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )

        order_nums_list = [form.instance.order_num for form in self.forms]

        for i, order_num in enumerate(order_nums_list):

            if not (1 <= order_num <= self.instance.QUESTION_MAX_LIMIT):
                raise ValidationError(
                    f'Question num must be from 1 to {self.instance.QUESTION_MAX_LIMIT} inclusive.'
                )
            if i == 0 and order_num != 1:
                raise ValidationError(
                    'First question num must be 1.'
                )
            elif i != 0 and order_num - order_nums_list[i - 1] != 1:
                raise ValidationError(
                    'Question num must increment 1 from previous.'
                )


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)
        # num_correct_answers = sum(lst)

        # num_correct_answers = sum(1 for form in self.forms if form.cleaned_data['is_correct'])

        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('You must select at least 1 option.')

        if num_correct_answers == len(self.forms):
            raise ValidationError('NOT allowed to select all options.')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ['text']


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
