from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    AppointmentSerializer,
    RequestSerializer,
    UserSerializer,
)
from .models import Appointment, Request, User
from .mixins import ObjectPermissionMixin


class AppointmentViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_serializer_context(self):
        self.request.data["doctor"] = self.request.user.pk

    def get_queryset(self):
        user = self.request.user
        user_groups = set(user.groups.all().values_list("name", flat=True))

        if "Admin" in user_groups:
            queryset = Appointment.objects.all()
        elif "Doctor" in user_groups:
            queryset = Appointment.objects.filter(doctor=user)
        else:
            queryset = Appointment.objects.filter(patient=user)
        return queryset


class RequestViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_serializer_context(self):
        self.request.data["patient"] = self.request.user.pk

    def get_queryset(self):
        user = self.request.user
        user_groups = set(user.groups.all().values_list("name", flat=True))

        if "Admin" in user_groups or "Doctor" in user_groups:
            queryset = Request.objects.all()
        else:
            queryset = Request.objects.filter(patient=user)
        return queryset


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        user_groups = set(user.groups.all().values_list("name", flat=True))

        if "Admin" in user_groups or "Doctor" in user_groups:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(email=user.email)
        return queryset
