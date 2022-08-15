from django.shortcuts import render
from accounts.models import User


# Create a function create context for use in views about_us and homepage
def context_dict(request):
    users = User.objects.all()
    context = dict()
    context['users'] = users
    context['user_site'] = None
    # if user login in site => context['user_site'] = info_user
    if request.user.is_authenticated:
        context['user_site'] = request.user

    return context


# Create fbv view page about_us
def about_us(request):
    context = context_dict(request)
    return render(request, 'about_us.html', context=context)


# Create fbv view page home
def homepage(request):
    context = context_dict(request)
    return render(request, 'homepage.html', context=context)
