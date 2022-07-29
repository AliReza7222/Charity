from django.shortcuts import render


def select_person(request):
    if request.method == 'GET':
        return render(request, 'select_ben_ch.html')