from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponse
from .models import User
from django.contrib.auth.hashers import make_password, check_password


from .models import User
from .forms import RegisterForm


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
            return HttpResponse("ok")
        return HttpResponse(form.errors.as_data())
