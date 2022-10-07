from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import ConversationSerializer, ConversationDetailSerializer, MessagesSerializer, MessagesDetailSerializer
from chat.models import Conversation, Messages


class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "conversation": reverse("chat_api:conversation_list", request=request),
            "messages": reverse("chat_api:message_list", request=request)
        })


api_root_view = ApiRootView.as_view()


class ConversationListCreateView(ListCreateAPIView):
    queryset = Conversation.active_objects.all()
    serializer_class = ConversationSerializer


conversation_list_view = ConversationListCreateView.as_view()
conversation_create_view = ConversationListCreateView.as_view()


class ConversationDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Conversation.active_objects.all()
    serializer_class = ConversationDetailSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


conversation_details_view = ConversationDetailUpdateDeleteView.as_view()
conversation_update_view = ConversationDetailUpdateDeleteView.as_view()
conversation_delete_view = ConversationDetailUpdateDeleteView.as_view()


class MessagesListCreateView(ListCreateAPIView):
    queryset = Messages.active_objects.all()
    serializer_class = MessagesSerializer


message_list_view = MessagesListCreateView.as_view()
message_create_view = MessagesListCreateView.as_view()


class MessageDetailUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Messages.active_objects.all()
    serializer_class = MessagesDetailSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


message_detail_view = MessageDetailUpdateView.as_view()
message_update_view = MessageDetailUpdateView.as_view()
message_delete_view = MessageDetailUpdateView.as_view()
