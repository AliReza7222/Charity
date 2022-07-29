from string import ascii_lowercase, ascii_uppercase, digits
import random

from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.http import HttpResponse
from .models import User, Token
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout


from .models import User
from .forms import RegisterForm, LoginForm
from .authenticate import UserBackend


class RegisterUser(CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = self.form_class(data)

        if form.is_valid():
            password_hash = make_password(form.cleaned_data.get('password'))
            post = form.save()
            post.password = password_hash
            post.save()
            context = {'form': self.form_class(), 'success': data.get('username')}
            return render(request, 'register.html', context=context)
        return render(request, 'register.html', context={'form': form})


class LoginUser(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username, password, email = data.get('username'), data.get('password'), data.get('email')
            user = UserBackend.authenticate(request, username=username, password=password, email=email)
            if user is not None:
                str_list = [i for i in (ascii_uppercase + ascii_lowercase + digits)]
                create_token = ''.join(random.choices(str_list, k=36))
                if not Token.objects.filter(user__username=username).exists():
                    Token.objects.create(user=user, token=create_token)
                login(request, user)
                return HttpResponse('login user')
        return render(request, 'login.html', context={'form': form})