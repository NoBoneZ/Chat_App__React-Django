from random import randint
import requests

from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserDetailSerializer, TokenSerializer
from accounts.models import User, ResetUserPassword
from helper.email import new_send_mail_func
from .permissions import IsOwner, IsStaff


class ApiRoot(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "user": reverse("accounts_api:api_user_list", request=request)
        })


api_root_view = ApiRoot.as_view()


class UserListCreateView(ListCreateAPIView):
    queryset = User.active_objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsStaff,)


user_list_view = UserListCreateView.as_view()
user_create_view = UserListCreateView.as_view()


class UserDetailsUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = User.active_objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "pk"
    permission_classes = (IsOwner,)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


user_detail_view = UserDetailsUpdateDelete.as_view()
user_update_view = UserDetailsUpdateDelete.as_view()
user_delete_view = UserDetailsUpdateDelete.as_view()


class UserAuthenticateView(APIView):
    permission_classes = (IsStaff,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.active_objects.get(username=username)
            email = user.email
        except User.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is not None:
            # serializer = UserSerializer(user, context={'request': request})
            endpoint = "http://localhost:7890/api/accounts/token/"
            response = requests.post(endpoint, json={"email": user.email, "password": password})
            context = {
                "refresh": response.json()["refresh"],
                "access": response.json()["access"]
            }
            # return Response(serializer.data, status=HTTP_200_OK)
            return Response(context, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


user_authenticate_view = UserAuthenticateView.as_view()


class ForgotPasswordAPIView(APIView):
    permission_classes = (IsStaff,)

    def post(self, request, *args, **kwargs):
        try:

            email = request.data.get("email")

            user = User.active_objects.get(email=email)
            if ResetUserPassword.objects.filter(user_id=user.id).first():
                raise ValidationError("Code already generated, New code cannot be generated")

            reset_password = ResetUserPassword.objects.create(user=user, token=randint(99, 99999))

            context = {
                "user": user,
                "token": reset_password.token,
            }

            email_body = {
                "subject": f"Password Reset Code for {user.username}",
                'recipients': email
            }

            new_send_mail_func(email_body, context)
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


forgot_password_view = ForgotPasswordAPIView.as_view()


class VerifyCodeAPIView(APIView):
    permission_classes = (IsStaff,)

    def post(self, request, *args, **kwargs):
        try:
            token = request.data.get("token")
            reset_password = ResetUserPassword.objects.get(token=token)
            uid = urlsafe_base64_encode(force_bytes(reset_password.user_id))
            reset_password.delete()
            context = {
                "uid": uid
            }
            print(uid)
            return Response(context, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


verify_code_view = VerifyCodeAPIView.as_view()


class ForgotPasswordChangePasswordAPIView(APIView):
    permission_classes = (IsStaff,)

    def post(self, request, *args, **kwargs):
        try:

            user_id = urlsafe_base64_decode(kwargs["uid"])
            user = User.active_objects.get(id=user_id)

            password1 = request.data.get("new_password")
            password2 = request.data.get("confirm_password")

            if password1 == "":
                raise ValidationError("Password field is required")

            if password1 == password2:
                user.password = make_password(password1)
                user.save()
                return Response(status=HTTP_200_OK)
            return Response({"message": "Password's don't match !"}, status=HTTP_400_BAD_REQUEST)
        except:
            return Response(status=HTTP_400_BAD_REQUEST)


forgot_change_password_view = ForgotPasswordChangePasswordAPIView.as_view()


class TokenObtainApiView(TokenObtainPairView):
    # permission_classes = (IsStaff,)
    serializer_class = TokenSerializer


token_obtain_view = TokenObtainApiView.as_view()
