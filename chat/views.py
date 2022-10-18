import datetime

from django.shortcuts import render, reverse
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View

from accounts.models import User
from .models import Conversation, Messages
from .forms import MessagesForm


# Create your views here.


def homepage(request):
    return render(request, "chat/home.html", )


class StartConversationView(View):
    def get(self, request, *args, **kwargs):

        conversation = Conversation.active_objects.filter(
            Q(starter=User.active_objects.get(id=request.user.id), second_party=User.active_objects.get(id=kwargs["pk"]))
            | Q(starter=User.active_objects.get(id=kwargs["pk"]), second_party=User.active_objects.get(id=request.user.id))).first()

        if conversation is None:
            conversation = Conversation.active_objects.create(starter=User.active_objects.get(id=request.user.id),
                                                              second_party=User.active_objects.get(id=kwargs["pk"])
                                                              )

        print(conversation)
        username = User.active_objects.get(id=kwargs["pk"])
        return HttpResponseRedirect(reverse("chat:conversation_messages", args=[conversation.id, username]))


def conversation_messages(request, pk, username):
    try:
        conversation = Conversation.active_objects.get(id=pk)
    except Conversation.DoesNotExist:
        messages.error(request, "Conversation Does Not Exist !")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    unread_messages = Messages.unread_objects.filter(conversation_id=pk)

    for unread_message in unread_messages:
        unread_message.is_read = True
        unread_message.save()

    # print(Messages.active_objects.all().first().date_sent.isoformat())
    # print(datetime.datetime.now().isoformat())

    if request.method == "POST":
        form = MessagesForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = User.active_objects.get(id=request.user.id)
            message.receiver = User.active_objects.get(username=username)
            message.save()

            messages.success(request, "Message sent successfully")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        errors = (form.errors.as_text()).split("*")
        messages.error(request, errors[len(errors) - 1])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    context = {
        "chat_messages": Messages.active_objects.filter(conversation_id=pk),
        "message_form": MessagesForm(),
        "second_party": username
    }
    return render(request, "chat/conversations.html", context)
