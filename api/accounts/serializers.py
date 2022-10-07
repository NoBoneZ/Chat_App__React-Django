from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.reverse import reverse

from accounts.models import User


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="accounts_api:api_user_details", lookup_field="pk", read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", 'gender', "url")


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "gender")
