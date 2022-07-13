from django.urls import path
from .views import UserRegistration, Logout, Login, register

urlpatterns = [
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('register_user/', UserRegistration.as_view()),
    path('register/', register)
]
