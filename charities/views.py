from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Benefactor, Charity, Task, ProfileUser
from .forms import BenefactorForm, CharityForm, ProfileForm
from .permissions import IsLoginUser


@login_required(login_url='/accounts/login/')
def select_person(request):
    if request.method == 'GET':
        return render(request, 'select_ben_ch.html')


@method_decorator(login_required, name='dispatch')
class BenefactorCreate(FormView):
    template_name = 'form_ben.html'
    form_class = BenefactorForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, free_time, exp = request.user, data.get('free_time_per_week'), data.get('experience')
            if Benefactor.objects.filter(user=user).exists():
                return HttpResponse('you create a object later ....')
            Benefactor.objects.create(user=user, experience=exp, free_time_per_week=free_time)
            return redirect('/charities/profile/')
        return HttpResponse(form.errors)


@method_decorator(login_required, name='dispatch')
class CharityCreate(FormView):
    template_name = 'form_ch.html'
    form_class = CharityForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, name, reg_number = request.user, data.get('name'), data.get('reg_number')
            if Charity.objects.filter(user=user).exists():
                return HttpResponse('you create a object later ....')
            Charity.objects.create(user=user, name=name, reg_number=reg_number)
            return redirect('/charities/profile/')
        return HttpResponse(form.errors)


@method_decorator(login_required, name='dispatch')
class CreateProfile(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user, img = request.user, request.FILES.get('image')
            phone, address, description = data.get('phone'), data.get('address'), data.get('description')
            ProfileUser.objects.create(user=user, phone=phone, address=address, description=description, image=img)
            return redirect('/home/')
        print(form.errors)
        return HttpResponse('error')
