from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from django.db.models import Q

from chat.models import Conversation, Messages
from accounts.models import User


class ConversationUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ConversationMessagesSerializer(ModelSerializer):
    sender = ConversationUserSerializer(read_only=True)
    receiver = ConversationUserSerializer(read_only=True)

    class Meta:
        model = Messages
        fields = ("sender", "receiver", "text", "date_sent")


class ConversationLastMessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = ("text", "images", "files")
        # extra_kwargs = {
        #     "images": {"read_only": True},
        #     "files": {"read_only": True},
        #     "text": {"read_only": True},
        # }


class ConversationSerializer(ModelSerializer):
    all_active_messages = HyperlinkedIdentityField(view_name="chat_api:conversation_messages", lookup_field='pk',
                                                   read_only=True)
    url = HyperlinkedIdentityField(view_name="chat_api:conversation_detail", lookup_field="pk", read_only=True)
    last_message = ConversationLastMessagesSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'id', "starter", "starter_username", "second_party", "second_party_username", "date_created",
            "all_active_messages", "last_message", 'url')


class ConversationDetailSerializer(ModelSerializer):
    all_active_messages = HyperlinkedIdentityField(view_name="chat_api:conversation_messages", lookup_field='pk',
                                                   read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', "starter", "starter_username", "second_party", "second_party_username", "date_created",
                  "all_active_messages",)
        extra_kwargs = {
            "starter": {"read_only": True},
            "second_party": {"read_only": True},
        }


class ConversationMessagesListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="chat_api:message_detail", lookup_field="pk")

    class Meta:
        model = Messages
        fields = ('id', "conversation", 'sender', 'receiver', "text", "images", "files", "date_sent", "url")
        # extra_kwargs = {
        #     "images": {"write_only": True},
        #     "files": {"write_only": True}
        # }


class MessagesSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="chat_api:message_detail", lookup_field="pk")

    class Meta:
        model = Messages
        fields = ('id', "conversation", 'sender', 'receiver', "text", "images", "files", "date_sent", "url")
        extra_kwargs = {
            "images": {"write_only": True},
            "files": {"write_only": True}
        }


class MessagesDetailSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = ('id', "conversation", 'sender', 'receiver', "text", "images", "files", "date_sent", 'is_read',)
        extra_kwargs = {
            'sender': {"read_only": True},
            "receiver": {"read_only": True}
        }

# class UserConversationMessagesSerializer(ModelSerializer):
#     url = HyperlinkedIdentityField(view_name="chat_api:message_detail", lookup_field="pk")
#
#     class Meta:
#         model = Messages
#         fields = ("conversation", 'sender', 'receiver', "text", "date_sent", 'is_read', "url")
#         extra_kwargs = {
#             "conversation": {"write_only": True},
#
#         }
