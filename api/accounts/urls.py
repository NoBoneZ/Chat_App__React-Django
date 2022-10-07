from django.urls import path

from .views import user_list_view, user_create_view, api_root_view, user_detail_view, user_delete_view, user_update_view

app_name = "accounts_api"

urlpatterns = [
    path("", api_root_view, name="api_root"),
    path("users_list/", user_list_view, name="api_user_list"),
    path("user_create/", user_create_view, name="api_user_create"),
    path("user/details/<int:pk>/", user_detail_view, name="api_user_details"),
    path("user/update/<int:pk>/", user_update_view, name="api_user_update"),
    path("user/delete/<int:pk>/", user_delete_view, name="api_user_delete"),
]
