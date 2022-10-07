from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import (ConversationSerializer, ConversationDetailSerializer,
                          MessagesSerializer, MessagesDetailSerializer
                          )
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

    def post(self, request, *args, **kwargs):
        starter = request.data.get("starter")
        second_party = request.data.get("second_party")
        if starter == second_party:
            raise ValidationError("The starter and the second party can not be the same party")
        elif Conversation.active_objects.filter(starter_id=starter, second_party_id=second_party).first() is not None:
            raise ValidationError("Conversation already exists")
        elif Conversation.active_objects.filter(starter_id=second_party, second_party_id=starter).first() is not None:
            raise ValidationError("Conversation already exists")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


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

    def post(self, request, *args, **kwargs):
        sender = int(request.data.get('sender'))
        receiver = int(request.data.get('receiver'))
        conversation = Conversation.active_objects.get(id=int(request.data.get('conversation')))
        if sender == receiver:
            raise ValidationError("the sender and the receiver cannot be the same person")
        elif (sender == conversation.starter or sender == conversation.second_party) and (receiver == conversation.starter or receiver == conversation.second_party):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        raise ValidationError("Invalid entry")


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
