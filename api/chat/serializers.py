from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

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


class ConversationSerializer(ModelSerializer):
    starter = ConversationUserSerializer()
    second_party = ConversationUserSerializer()
    all_active_messages = ConversationMessagesSerializer(read_only=True, many=True)
    url = HyperlinkedIdentityField(view_name="chat_api:conversation_detail", lookup_field="pk", read_only=True)

    class Meta:
        model = Conversation
        fields = ("starter", "second_party", "date_created", "all_active_messages", 'url')


class ConversationDetailSerializer(ModelSerializer):
    starter = ConversationUserSerializer()
    second_party = ConversationUserSerializer()
    all_active_messages = ConversationMessagesSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ("starter", "second_party", "date_created", "all_active_messages",)


class MessagesSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="chat_api:message_detail", lookup_field="pk")

    class Meta:
        model = Messages
        fields = ("conversation", "text", "date_sent", 'is_read', "url")


class MessagesDetailSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = ("conversation", "text", "date_sent", 'is_read', )
