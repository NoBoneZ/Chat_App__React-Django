from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q


from chat.models import Conversation

# Create your models here.

class ActiveManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class InactiveManager(UserManager):

    def get_queryset(self):
        return super(InactiveManager, self).get_queryset().filter(is_active=False)


class User(AbstractUser):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Prefer Not To Say", "Prefer not to say")
    )

    STATUS_CHOICES = (
        ("Available", "Available"),
        ("Away", "Away"),
        ("Offline", "Offline"),
    )
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, unique=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    profile_picture = models.ImageField(null=True, upload_to="profile_picture/", default="avatar.svg")
    about = models.CharField(max_length=200, null=True, default="I'm Awesome!", blank=True)
    status = models.CharField(null=True, choices=STATUS_CHOICES, default="Offline", max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    active_objects = ActiveManager()
    not_active_objects = InactiveManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    def __str__(self):
        return self.username

    @property
    def user_conversations(self):
        return Conversation.active_objects.filter(Q(starter_id=self.id) | Q(second_party_id=self.id))
