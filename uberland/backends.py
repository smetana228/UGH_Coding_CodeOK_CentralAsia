from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number, first_name, last_name, **kwargs):
        try:
            user = CustomUser.objects.get(first_name = first_name, last_name=last_name, phone_number=phone_number)
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None