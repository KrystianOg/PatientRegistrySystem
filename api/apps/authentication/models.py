import json
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from guardian.shortcuts import assign_perm
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # base fields
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
        return (
            self.first_name + " " + self.last_name
            if self.first_name and self.last_name
            else self.email.split("@")[0]
        )

    def get_token(self):
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @property
    def types(self):
        values = self.groups.values_list("name", flat=True)
        return json.dumps(list(values), cls=DjangoJSONEncoder)

    @property
    def is_doctor(self):
        return self.groups.filter(name="Doctor").exists()

    @property
    def is_patient(self):
        return self.groups.filter(name="Patient").exists()


# Create auth token post User save
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def assign_permissions(sender, instance, created=False, **kwargs):
    if created:
        assign_perm("change_user", instance, instance)
        assign_perm("delete_user", instance, instance)
