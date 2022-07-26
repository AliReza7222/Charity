from django.shortcuts import render
from accounts.models import User


def about_us(request):
    users = User.objects.all()
    context = dict()
    context['users'] = users

    if request.method == 'GET':
        return render(request, 'about_us.html', context=context)