from string import ascii_lowercase, ascii_uppercase, digits
import random

from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout
from django .contrib import messages


from .models import User, Token
from .forms import RegisterForm, LoginForm, ChangePasswordForm
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
                if not Token.objects.filter(user__username=username).exists():
                    str_list = [i for i in (ascii_uppercase + ascii_lowercase + digits)]
                    create_token = ''.join(random.choices(str_list, k=36))
                    Token.objects.create(user=user, token=create_token)
                login(request, user)
                messages.success(request, f'{username} وارد سایت شدید .')
                return redirect('/home/')
        return render(request, 'login.html', context={'form': form})


@login_required(login_url='/accounts/login/')
def logout_user(request):
    if request.method == "GET":
        return render(request, 'logout.html', context={'user': request.user})
    if request.method == 'POST':
        if request.user.is_authenticated:
            token_user = Token.objects.get(user=request.user)
            token_user.delete()
            logout(request)
            messages.success(request, 'شما با موفقیت از سایت خارج شدید .')
            return redirect('/home/')


class ChangePassword(FormView):
    model = User
    template_name = 're_password.html'
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_password = data.get('password_new')
            email = data.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            message = 'رمز عبور شما با موفقیت تغییر یافت .'
            messages.success(request, message)
            return redirect('/home/')
        return render(request, 're_password.html', context={'form': form})

