from django.contrib.auth.hashers import check_password
from .models import User


class UserBackend:

    def authenticate(self, username=None, password=None, email=None):
        try:
            user = User.objects.get(username=username)
            check_email = User.objects.filter(email=email).exists()
            check_password_user = check_password(password, user.password)
            if check_email and check_password_user:
                return user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
