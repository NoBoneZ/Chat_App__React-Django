from django.urls import path


from .views import (conversation_list_view, conversation_create_view,
                    api_root_view, conversation_update_view,
                    conversation_details_view, conversation_delete_view,
                    message_list_view, message_create_view, message_detail_view,
                    message_update_view, message_delete_view
                    )

app_name = "chat_api"


urlpatterns = [
    path("", api_root_view, name="api_root"),
    path("conversation_list/", conversation_list_view, name="conversation_list"),
    path("conversation/create/", conversation_create_view, name="conversation_create"),
    path("conversation/<int:pk>/details/", conversation_details_view, name="conversation_detail"),
    path("conversation/<int:pk>/update/", conversation_update_view, name="conversation_update"),
    path("conversation/<int:pk>/delete/", conversation_delete_view, name="conversation_delete"),
    path("message_list/", message_list_view, name="message_list"),
    path("message/create/", message_create_view, name="message_create"),
    path("message/<int:pk>/details/", message_detail_view, name="message_detail"),
    path("message/<int:pk>/update/", message_update_view, name="message_update"),
    path("message/<int:pk>/delete/", message_delete_view, name="message_delete"),
]