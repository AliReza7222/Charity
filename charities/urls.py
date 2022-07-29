from django.urls import path
from .views import select_person, BenefactorCreate, CharityCreate


urlpatterns = [
    path('select/', select_person, name='select'),
    path('benefactor/', BenefactorCreate.as_view(), name='benefactor'),
    path('charity', CharityCreate.as_view(), name='charity')
]
