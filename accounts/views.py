from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.contrib.auth.hashers import check_password, make_password

from .models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import obtain_auth_token


from .forms import Register, LogoutUser
from .serializers import UserSerializer


class Login(LoginView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        return obtain_auth_token(request)


class Logout(FormView):
    template_name = 'logout.html'
    form_class = LogoutUser

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            try:
                user.auth_token.delete()
                return HttpResponse(f'Bye {user.username}.....')
            except:
                return HttpResponse("This user don't login....", status=status.HTTP_404_NOT_FOUND)
        return HttpResponse("username or password invalid.....", status=status.HTTP_404_NOT_FOUND)


class UserRegistration(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        form = Register()
        context = {'form': form}
        return render(request, 'register_user.html', context=context)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return HttpResponse(f"<h3>Register user with fullname : "
                                f"{user.get('first_name')}-{user.get('last_name')}</h3>"
                                f"<br><a href='/'>Home</a>")
        return Response(data='Error.....', status=400)


def register(request):
    context = {'data': [1, 2, 3, 4]}
    return render(request, 'base_register.html', context=context)
