import re
from django import forms
from django.contrib.auth.hashers import check_password

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from .models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            're_password',
            'first_name',
            'last_name',
            'email',
            'age',
            'gender'
        ]
        labels = {
            'username': 'نام کاربری',
            'password': 'رمز',
            're_password': 'تکرار رمز',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'email': 'ایمیل',
            'age': 'سن',
            'gender': 'جنسیت',
        }
        help_texts = {'username': ''}
        widgets = {
            'username': forms.TextInput(attrs={"placeholder": "لطفا نام کاربری خود را وارد کنید"}),
            'password': forms.PasswordInput(attrs={"placeholder": " رمز را وارد کنید"}),
            're_password': forms.PasswordInput(attrs={"placeholder": "لطفا رمز عبور را تکرار کنید"}),
            'first_name': forms.TextInput(attrs={"placeholder": "اسم "}),
            'last_name': forms.TextInput(attrs={"placeholder": " نام خانوادگی "}),
            'email': forms.EmailInput(attrs={"placeholder": "ایمیل"}),
            'age': forms.NumberInput(attrs={"placeholder": "سن "}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلا ثبت شده است .")
        if len(username) < 4:
            raise forms.ValidationError("نام کاربری باید بیشتر از 4 حرف باشد .")
        if not(re.findall('(?=.*[a-z])(?=.*[0-9]).+', username)):
            raise forms.ValidationError('نام کاربری باید متشکل از حروف و اعداد باشد .')
        return username

    def clean_re_password(self):
        data = self.cleaned_data
        password, re_password = data.get('password'), data.get('re_password')

        if password != re_password:
            raise forms.ValidationError('رمز عبور با تکرار ان برابر نیست !')

        if len(password) < 7:
            raise forms.ValidationError('طول رمز باید حداقل 7 کارکتر باشد !')
        return re_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('نام کاربری دیگری با این ایمیل قبلا ثبت شده !')
        return email


class LoginForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    username = forms.CharField(label='نام کاربری / پسورد',
                               widget=forms.TextInput(attrs={"placeholder": "لطفا نام کاربری خود را وارد کنید"}))
    password = forms.CharField(label='نام کاربری / پسورد',
                               widget=forms.PasswordInput(attrs={"placeholder": " رمز را وارد کنید"}))
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={"placeholder": "ایمیل"}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('نام کاربری یا پسورد اشتباه است .')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            user_password = User.objects.get(username=self.cleaned_data.get('username')).password
            if check_password(password, user_password):
                return password
            raise forms.ValidationError('نام کاربری یا پسورد اشتباه است .')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            user_email = User.objects.get(username=self.cleaned_data.get('username')).email
            if email == user_email:
                return email
            raise forms.ValidationError('این ایمیل برای این نام کاربری نامعتبر است !')
