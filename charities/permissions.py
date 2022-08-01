from accounts.models import User
from django.core import validators
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
