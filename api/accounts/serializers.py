from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, CharField
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password

from accounts.models import User
from chat.models import Conversation
from ..chat.serializers import ConversationSerializer, ConversationUserSerializer, ConversationMessagesSerializer


class UserConversationSerializer(ModelSerializer):
    starter = ConversationUserSerializer()
    second_party = ConversationUserSerializer()
    url = HyperlinkedIdentityField(view_name="chat_api:conversation_detail", lookup_field="pk", read_only=True)

    class Meta:
        model = Conversation
        fields = ("starter", "second_party", "date_created", 'url')


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="accounts_api:api_user_details", lookup_field="pk", read_only=True)
    user_conversations = UserConversationSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("username", "email", 'gender', "url", 'password', 'user_conversations')

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.gender = validated_data.get("gender", instance.gender)
        # instance.password = make_password(validated_data["password"])
        instance.save()
        return instance


class UserDetailSerializer(ModelSerializer):
    # password = CharField(max_length=20, )

    class Meta:
        model = User
        fields = ("username", "email", "gender",)
