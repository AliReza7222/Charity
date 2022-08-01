import re

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
    phone = forms.CharField(label='شماره تلفن همراه')
    address = forms.CharField(max_length=300, label='ادرس',
                              widget=forms.TextInput(attrs={"placeholder": "ادرس خود را وارد کنید "}))
    description = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "درباره خود بنویسید "}), label='توضیحات')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) == 11 and re.findall('^09[0-9]+', phone):
            return phone
        elif len(phone) == 13 and re.findall('^\+989[0-9]+', phone):
            return phone
        elif len(phone) == 14 and re.findall('^0{2}989[0-9]+', phone):
            return phone
        raise forms.ValidationError('شماره تلفن همراه را بصورت صحیح وارد کنید !')


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'state',
            'description'
        ]
        labels = {
            'title': 'عنوان',
            'state': 'جالت',
            'description': 'توضیح',
        }