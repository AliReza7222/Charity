from django import forms
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
        return username

    def clean_re_password(self):
        data = self.cleaned_data
        password, re_password = data.get('password'), data.get('re_password')

        if password == re_password:
            return re_password
        raise forms.ValidationError('رمز عبور با تکرار ان برابر نیست !')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('نام کاربری دیگری با این ایمیل قبلا ثبت شده !')
        return email


