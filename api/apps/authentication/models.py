from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.IntegerChoices):
        ADMIN = (1, "Admin")
        MODERATOR = (2, "Moderator")
        DOCTOR = (3, "Doctor")
        PATIENT = (4, "Patient")

    # base fields
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.PATIENT)

    # personal information
    email = models.EmailField(max_length=320, unique=True)
    first_name = models.CharField(max_length=63, blank=True, null=True)
    last_name = models.CharField(max_length=63, blank=True, null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def username(self):
        return self.first_name + " " + self.last_name if self.first_name and self.last_name \
            else self.email.split("@")[0]

    @property
    def type_detail(self):
        return self.get_type_display()

    @property
    def type_detail(self):
        return self.get_type_display()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
