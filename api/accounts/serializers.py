from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, CharField
from rest_framework.reverse import reverse
from django.contrib.auth.hashers import make_password

from accounts.models import User


class UserSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="accounts_api:api_user_details", lookup_field="pk", read_only=True)

    # password = CharField(max_length=20,)

    class Meta:
        model = User
        fields = ("username", "email", 'gender', "url", 'password')

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
