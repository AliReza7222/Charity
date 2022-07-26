from django.urls import path
from .views import about_us, homepage


name = 'about_us'
urlpatterns = [
    path('about', about_us, name='about'),
    path('home', homepage, name='home'),
]
