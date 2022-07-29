from django.shortcuts import render
from accounts.models import User


def context_dict():
    users = User.objects.all()
    context = dict()
    context['users'] = users
    return context


def about_us(request):
    context = context_dict()

    if request.method == 'GET':
        return render(request, 'about_us.html', context=context)


def homepage(request):
    context = context_dict()
    context['user_site'] = None
    if request.user.is_authenticated:
        context['user_site'] = request.user

    return render(request, 'homepage.html', context=context)
