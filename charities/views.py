from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Benefactor, Charity, Task, ProfileUser
from .forms import BenefactorForm, CharityForm, ProfileForm, TaskForm
from .permissions import check_charity_user, check_benefactor


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
    template_name = 'tasks.html'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user_charity = Charity.objects.get(user=user)
            state, title, description = data.get('state'), data.get('title'), data.get('description')
            Task.objects.create(charity=user_charity, state=state, title=title, description=description)
            messages.success(request, 'تسک شما با موفقیت ثبت شد .')
            return redirect('/charities/task/')
        return render(request, 'tasks.html', context={'form': form})


def show_tasks(request):
    charities = Charity.objects.all()

    if request.method == "GET":
        context = {'charities': charities}
        return render(request, 'list_taskes.html', context=context)


@check_benefactor
@login_required(login_url='/accounts/login/')
def task_request(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'GET':
        if task.state != 'P':
            messages.error(request, 'شما نمیتوانید این نیکوکاری را قبول کنید چون در وضعیت Pending نیست .')
            return redirect('/charities/show_taskes/')
        context = {'task': task}
        return render(request, 'request_task.html', context=context)
    if request.method == 'POST':
        benefactor = Benefactor.objects.get(user=request.user)
        task.assign_to_benefactor(benefactor)
        messages.success(request, 'درخواست نیکوکاری شما ثبت شد منتظر جواب بمانید .')
        return redirect('/home/')
