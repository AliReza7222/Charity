from django.urls import path
from .views import select_person, BenefactorCreate


urlpatterns = [
    path('select/', select_person, name='select'),
    path('benefactor/', BenefactorCreate.as_view(), name='benefactor')
]
