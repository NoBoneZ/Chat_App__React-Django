from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    class Meta:
        form = CustomUserChangeForm

        fieldsets = (('Main Information',
                      {"fields": (
                          "first_name", "last_name", "profile_picture", "username", "phone_number")}),
                     ("addresses", {"fields": ("email",)}),
                     ("others", {"fields": ("last_login",)})
                     )

        list_display = ["first_name", "last_name", "email", "username"]
        ordering = ["first_name"]


admin.site.register(User, CustomUserAdmin)
