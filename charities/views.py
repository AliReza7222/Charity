from django.shortcuts import render
from django.views.generic import FormView
from django.http import HttpResponse

from .models import Benefactor, Charity, Task
from .forms import BenefactorForm, CharityForm


def select_person(request):
    if request.method == 'GET':
        return render(request, 'select_ben_ch.html')


class BenefactorCreate(FormView):
    model = Benefactor
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
            return HttpResponse('create ben')
        return HttpResponse(form.errors)


class CharityCreate(FormView):
    model = Charity
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
            return HttpResponse('create che')
        return HttpResponse(form.errors)
