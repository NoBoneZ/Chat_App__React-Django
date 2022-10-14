from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (user_list_view, user_create_view,
                    api_root_view, user_detail_view,
                    user_delete_view, user_update_view,
                    user_authenticate_view, forgot_change_password_view,
                    forgot_password_view, verify_code_view, token_obtain_view
                    )

app_name = "accounts_api"

urlpatterns = [
    path("", api_root_view, name="api_root"),
    path("users_list/", user_list_view, name="api_user_list"),
    path("user_create/", user_create_view, name="api_user_create"),
    path("user/details/<int:pk>/", user_detail_view, name="api_user_details"),
    path("user/update/<int:pk>/", user_update_view, name="api_user_update"),
    path("user/delete/<int:pk>/", user_delete_view, name="api_user_delete"),

    path("user_authenticate/", user_authenticate_view, name="user_authenticate"),


    path("forgot_password/", forgot_password_view, name="forgot_password"),
    path("verify_code/", verify_code_view, name="verify_code"),
    path("forgot_password_change_password/<str:uid>/", forgot_change_password_view, name="forgot_password"),
    path("token_refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", token_obtain_view, name="token")

]
