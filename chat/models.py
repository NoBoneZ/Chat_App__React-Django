from django.db import models

# from accounts.models import User
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class ActiveManager(models.Manager):

    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class InactiveManager(models.Manager):

    def get_queryset(self):
        return super(InactiveManager, self).get_queryset().filter(is_active=False)


class ReadManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_read=True)


class UnreadManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)


class ChatBox(models.Model):
    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    starter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="starter")
    second_party = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="second_party")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveManager()
    not_active_objects = InactiveManager()

    class Meta:
        ordering = ("-date_created",)

    @property
    def all_active_messages(self):
        return Messages.active_objects.filter(conversation_id=self.id).order_by("date_sent")


class Messages(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    text = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to="conversation_images/", blank=True)
    files = models.FileField(upload_to="conversation_files/", blank=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveManager()
    not_active_objects = InactiveManager()
    read_objects = ReadManager()
    unread_objects = UnreadManager()

    class Meta:
        ordering = ("date_sent",)
