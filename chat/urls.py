from django.urls import path

from .views import homepage, conversation_messages, StartConversationView

app_name = "chat"

urlpatterns = [
    path("", homepage, name="home"),
    path("start_conversation/<int:pk>", StartConversationView.as_view(), name="start_conversation"),
    path("conversation/<int:pk>/<str:username>", conversation_messages, name="conversation_messages")
]
