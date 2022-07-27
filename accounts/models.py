from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICE_GENDER = [
        ('M', 'مرد'),
        ('F', 'زن')
    ]
    re_password = models.CharField(max_length=20)
    age = models.PositiveIntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER, null=True, blank=True)


class Token(models.Model):
    token = models.CharField(max_length=36)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'token {}'.format(self.user.username)
