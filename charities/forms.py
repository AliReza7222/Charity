from django import forms

from .models import Benefactor, Charity, Task, ProfileUser


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


class ProfileForm(forms.Form):
    image = forms.ImageField(label='عکس پروفایل')
    phone = forms.CharField(label='شماره همراه')
    address = forms.CharField(max_length=300, label='ادرس',
                              widget=forms.TextInput(attrs={"placeholder": "ادرس خود را وارد کنید "}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "درباره خود بنویسید "}), label='توضیحات')
