from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import View

from .models import User
from .forms import CustomUserCreationForm


# Create your views here.


class SignInView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/sign_in.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.active_objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, f"User does not exist !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}")
            return HttpResponseRedirect(reverse("chat:home"))
        messages.error(request, "invalid Username or Password")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.title()
            user.email = user.email.lower()
            user.save()

            messages.info(request, "You need to log in !")
            return HttpResponseRedirect(reverse("accounts:sign_in"))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
    return render(request, "accounts/sign_up.html", {"form": CustomUserCreationForm()})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:sign_in"))
