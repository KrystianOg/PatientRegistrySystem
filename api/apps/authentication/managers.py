from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, Permission


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        try:
            user.groups.add(Group.objects.get(name="Patient"))
        except Group.DoesNotExist:
            Group.objects.create(name="Patient")
            user.groups.add(Group.objects.get(name="Patient"))

        user.user_permissions.add(Permission.objects.get(codename="add_request"))

        return user

    def create_doctor(self, email, password):
        if password is None:
            raise TypeError("Doctors must have a password.")

        user = self.create_user(email, password)

        try:
            user.groups.add(Group.objects.get(name="Doctor"))
        except Group.DoesNotExist:
            Group.objects.create(name="Doctor")
            user.groups.add(Group.objects.get(name="Doctor"))

        user.user_permissions.add(Permission.objects.get(codename="add_appointment"))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email address.")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        try:
            user.groups.add(Group.objects.get(name="Admin"))
        except Group.DoesNotExist:
            Group.objects.create(name="Admin")
            user.groups.add(Group.objects.get(name="Admin"))

        user.save(using=self._db)
        return user

    # TODO: maybe add a method to create a doctor or a patient
