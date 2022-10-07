from django.db.models import Q

from .models import Conversation
from accounts.models import User


def get_chat_list(request):
    context = {}

    if request.user.is_authenticated:
        search = request.GET.get("search_for_user") if request.GET.get("search_for_user") is not None else ""
        # conversations =
        context["chat_buddies"] = Conversation.active_objects.filter(Q(Q(starter_id=request.user.id)
                                                                       | Q(second_party_id=request.user.id)
                                                                       )
                                                                     & Q(Q(starter__username__icontains=search)
                                                                         | Q(second_party__username__icontains=search))
                                                                     )

        context["accounts"] = User.active_objects.filter(Q(username__icontains=search))
        context["checker"] = False if search == "" else True
        return context
    return context
