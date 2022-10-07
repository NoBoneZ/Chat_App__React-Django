from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "accounts": reverse("accounts_api:api_root", request=request),
            "chat": reverse("chat_api:api_root", request=request)
        })


api_root_view = ApiRoot.as_view()
