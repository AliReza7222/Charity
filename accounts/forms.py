from .models import User
from django import forms


class Register(forms.ModelForm):

    class Meta:
       model = User
       fields = ['username', 'password', 'email', 'first_name', 'last_name',
                 'phone', 'gender', 'age', 'description', 'address']


class LogoutUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

