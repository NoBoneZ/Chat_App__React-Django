from django.urls import path


from .views import api_root_view


app_name = "api"

urlpatterns = [
    path("", api_root_view, name='api_root'),
]