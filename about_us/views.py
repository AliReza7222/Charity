from django.shortcuts import render
from accounts.models import User
from django.contrib.auth import logout


def context_dict(request):
    users = User.objects.all()
    context = dict()
    context['users'] = users
    context['user_site'] = None
    if request.user.is_authenticated:
        context['user_site'] = request.user

    return context


def about_us(request):
    context = context_dict(request)
    return render(request, 'about_us.html', context=context)


def homepage(request):
    context = context_dict(request)
    return render(request, 'homepage.html', context=context)
