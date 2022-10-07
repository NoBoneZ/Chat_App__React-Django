from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .serializers import UserSerializer, UserDetailSerializer
from accounts.models import User


class ApiRoot(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "user": reverse("accounts_api:api_user_list", request=request)
        })


api_root_view = ApiRoot.as_view()


class UserListCreateView(ListCreateAPIView):
    queryset = User.active_objects.all()
    serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.password = make_password(serializer.password)
    #         serializer.save()
    #         return Response(serializer.data, status=HTTP_200_OK)
    #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


user_list_view = UserListCreateView.as_view()
user_create_view = UserListCreateView.as_view()


class UserDetailsUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = User.active_objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


user_detail_view = UserDetailsUpdateDelete.as_view()
user_update_view = UserDetailsUpdateDelete.as_view()
user_delete_view = UserDetailsUpdateDelete.as_view()
