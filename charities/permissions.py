from django.contrib import messages
from django.core import validators
from django.shortcuts import redirect
from django.http import HttpResponse


def check_charity_user(func):
    def check(request, *args, **kwargs):
        user = request.user
        if user.is_benefactor:
            message = '! شما بعنوان نیکوکار در این سایت هستید و متاسفانه نمیتوانید وارد این بخش سایت شوید '
            raise validators.ValidationError(message)
        else:
            return func(request, *args, **kwargs)
    return check


def check_benefactor(func):
    def check(request, *args, **kwargs):
        if request.user.is_anonymous:
            message = 'شما فقط قابلیت دیدن این صفحه را دارید برای استفاده از این صفحه اول وارد اکانت خود شوید .'
            messages.error(request, message=message)
            return redirect('/charities/show_taskes/')
        elif request.user.is_benefactor:
            return func(request, *args, **kwargs)
        elif request.user.is_charity:
            message = 'متاسفانه شما نمیتوانید وارد این صفحه شوید چون بعنوان موسسه خیریه در این سایت ثبت شدید .'
            raise validators.ValidationError(message)

    return check
