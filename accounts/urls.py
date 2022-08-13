from django.urls import path
from .views import RegisterUser, LoginUser, logout_user, ChangePassword


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password')
]
