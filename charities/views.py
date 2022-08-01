from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Benefactor, Charity, Task, ProfileUser
from .forms import BenefactorForm, CharityForm, ProfileForm
from .permissions import check_charity_user


@login_required(login_url='/accounts/login/')
def select_person(request):
    if request.method == 'GET':
        user = request.user
        if ProfileUser.objects.filter(user=request.user).exists():
            context = dict()
            if Benefactor.objects.filter(user=user).exists():
                context['benefactor'] = Benefactor.objects.get(user=user)
            elif Charity.objects.filter(user=user).exists():
                context['charity'] = Charity.objects.get(user=user)
            context['profile'] = ProfileUser.objects.get(user=user)
            return render(request, 'show_profile.html', context=context)
        if Benefactor.objects.filter(user=user).exists() or Charity.objects.filter(user=user).exists():
            return redirect('/charities/profile/')
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
        messages.success(request, 'شما نوع کاربری خود را قبلا انتخاب کردید .')
        return redirect('/home/')


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
        if form.errors:
            return render(request, 'form_ch.html', context={'form': form})
        messages.success(request, 'شما نوع کاربری خود را قبلا انتخاب کردید .')
        return redirect('/home/')


@method_decorator(login_required, name='dispatch')
class CreateProfile(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            user, img = request.user, request.FILES.get('image')
            phone, address, description = data.get('phone'), data.get('address'), data.get('description')
            # create profile
            if not ProfileUser.objects.filter(user=user).exists():
                ProfileUser.objects.create(user=user, phone=phone, address=address, description=description, image=img)
                messages.success(request, 'پروفایل کاربری شما کامل شد از بخش پروفایل میتوانید انرا ببینید .')
                return redirect('/home/')
            # update profile
            else:
                profile = ProfileUser.objects.get(user=user)
                profile.delete()
                ProfileUser.objects.create(user=user, phone=phone, address=address, description=description, image=img)
                return redirect('/charities/select/')

        return render(request, 'profile.html', context={'form': form})


@method_decorator([login_required, check_charity_user], name='dispatch')
class CreateTask(FormView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello')
