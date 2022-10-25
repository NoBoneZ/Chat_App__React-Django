from django.urls import re_path

from .consumers import ConversationConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', ConversationConsumer.as_asgi())
]
