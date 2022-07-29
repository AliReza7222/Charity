from django.shortcuts import render
from django.views.generic import CreateView
from django.http import HttpResponse

from .models import Benefactor, Charity, Task
from .forms import BenefactorForm


def select_person(request):
    if request.method == 'GET':
        return render(request, 'select_ben_ch.html')


class BenefactorCreate(CreateView):
    model = Benefactor
    template_name = 'form_ben.html'
    form_class = BenefactorForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user, free_time, exp = request.user, data.get('free_time_per_week'), data.get('experience')
            Benefactor.objects.create(user=user, experience=exp, free_time_per_week=free_time)
            return HttpResponse('create ben')
        return HttpResponse(form.errors)
