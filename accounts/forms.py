from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ("date_joined", "last_login", "superuser_status", "staff_status", "is_active", "password",
                   "phone_number"
                   )

        labels = {
            "password1": "Password",
            "password2": "Password Confirmation"
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "profile_picture",
                  "phone_number", "gender",
                  )
