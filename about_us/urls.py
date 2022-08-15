from django.urls import path
from .views import about_us, homepage

# Create url path for views app about_us
name = 'about_us'
urlpatterns = [
    path('about/', about_us, name='about'),
    path('home/', homepage, name='home'),
]
