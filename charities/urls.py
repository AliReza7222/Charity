from django.urls import path
from .views import select_person


urlpatterns = [
    path('select/', select_person, name='select')
]
