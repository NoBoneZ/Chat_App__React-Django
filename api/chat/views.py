from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q

from .serializers import (ConversationSerializer, ConversationDetailSerializer,
                          MessagesSerializer, MessagesDetailSerializer, ConversationMessagesListSerializer
                          )
from chat.models import Conversation, Messages
from accounts.models import User


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


class UserConversationsListCreateView(ListCreateAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.active_objects.all()

    def get(self, request, **kwargs):
        queryset = self.get_queryset().filter(Q(starter_id=kwargs["pk"]) | Q(second_party_id=kwargs["pk"]))
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        starter = int(request.data.get("starter"))
        second_party = int(request.data.get("second_party"))
        if starter != int(kwargs["pk"]):
            raise ValidationError("Invalid entry")
        elif self.get_queryset().filter(Q(starter_id=starter, second_party_id=second_party)
                                        | Q(second_party_id=starter, starter_id=second_party)).first():
            raise ValidationError("Conversation already exist")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.data, status=HTTP_400_BAD_REQUEST)


user_conversation_listview = UserConversationsListCreateView.as_view()
user_conversation_create_view = UserConversationsListCreateView.as_view()


class MessagesListCreateView(ListCreateAPIView):
    queryset = Messages.active_objects.all()
    serializer_class = MessagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        sender = int(request.data.get('sender'))
        receiver = int(request.data.get('receiver'))
        conversation = Conversation.active_objects.get(id=int(request.data.get('conversation')))
        if sender == receiver:
            raise ValidationError("the sender and the receiver cannot be the same person")
        elif (sender == conversation.starter or sender == conversation.second_party) and (
                receiver == conversation.starter or receiver == conversation.second_party):
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
    parser_classes = (MultiPartParser, FormParser)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


message_detail_view = MessageDetailUpdateView.as_view()
message_update_view = MessageDetailUpdateView.as_view()
message_delete_view = MessageDetailUpdateView.as_view()


class ConversationMessageListView(ListCreateAPIView):
    queryset = Messages.active_objects.all()
    serializer_class = ConversationMessagesListSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(conversation_id=kwargs["pk"])
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        sender = int(request.data.get("sender"))
        receiver = int(request.data.get("receiver"))
        conversation_check = int(request.data.get("conversation"))
        conversation = Conversation.active_objects.get(id=kwargs["pk"])

        if conversation_check != int(conversation.id):
            raise ValidationError("Invalid Conversation")
        elif sender == receiver:
            raise ValidationError("Sender and Receiver cannot be the same person")
        elif (sender == conversation.starter_id or sender == conversation.second_party_id) and (
                receiver == conversation.starter_id or receiver == conversation.second_party_id):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        raise ValidationError("Invalid input")


conversation_messages_listview = ConversationMessageListView.as_view()
conversation_messages_create_view = ConversationMessageListView.as_view()
