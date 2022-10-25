from django.urls import path

from .views import SignInView, sign_up, sign_out

app_name = "accounts"

urlpatterns = [
    path("sign_in/", SignInView.as_view(), name="sign_in"),
    path("sign_up/", sign_up, name="sign_up"),
    path("sign_out", sign_out, name="sign_out"),
]