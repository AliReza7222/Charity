from django import forms
from .models import Benefactor


class BenefactorForm(forms.ModelForm):

    class Meta:
        model = Benefactor
        fields = "__all__"
