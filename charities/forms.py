from django import forms

from .models import Benefactor, Charity, Task


class BenefactorForm(forms.ModelForm):

    class Meta:
        model = Benefactor
        fields = [
            'experience',
            'free_time_per_week'
        ]


class CharityForm(forms.ModelForm):

    class Meta:
        model = Charity
        fields = [
            'reg_number',
            'name'
        ]
