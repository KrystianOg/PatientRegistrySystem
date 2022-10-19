from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    AppointmentSerializer,
    RequestSerializer,
    UserSerializer,
)
from .models import Appointment, Request, User
from .mixins import ObjectPermissionMixin
from django.core.exceptions import PermissionDenied


class AppointmentViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_serializer_context(self):
        self.request.data["doctor"] = self.request.user.pk

    def get_queryset(self):
        user = self.request.user
        user_groups = set(user.groups.values_list("name", flat=True))

        if "Admin" in user_groups:
            queryset = Appointment.objects.all()
        elif "Doctor" in user_groups:
            queryset = Appointment.objects.filter(doctor=user)
        else:
            queryset = Appointment.objects.filter(patient=user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        doctor_pk = Appointment.objects.get(pk=int(kwargs["pk"])).doctor
        patient_pk = Appointment.objects.get(pk=int(kwargs["pk"])).patient
        if patient_pk != self.request.user.pk and doctor_pk != self.request.user.pk:
            raise PermissionDenied
        return super().destroy(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        patient_pk = Appointment.objects.get(pk=int(kwargs["pk"])).patient
        doctor_pk = Appointment.objects.get(pk=int(kwargs["pk"])).doctor
        if patient_pk != self.request.user.pk and doctor_pk != self.request.user.pk:
            raise PermissionDenied
        return super().retrieve(request, args, kwargs)


class RequestViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_serializer_context(self):
        self.request.data["patient"] = self.request.user.pk

    def get_queryset(self):
        user = self.request.user
        user_groups = set(user.groups.values_list("name", flat=True))

        if "Admin" in user_groups or "Doctor" in user_groups:
            queryset = Request.objects.all()
        else:
            queryset = Request.objects.filter(patient=user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        patient_pk = Request.objects.get(pk=int(kwargs["pk"])).patient
        if patient_pk != self.request.user.pk:
            raise PermissionDenied
        return super().destroy(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        user_groups = set(user.groups.values_list("name", flat=True))
        patient_pk = Request.objects.get(pk=int(kwargs["pk"])).patient
        if "Patient" in user_groups and patient_pk != self.request.user.pk:
            raise PermissionDenied
        return super().retrieve(request, args, kwargs)


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
        user_groups = set(user.groups.values_list("name", flat=True))

        if "Admin" in user_groups or "Doctor" in user_groups:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(email=user.email)
        return queryset

    def update(self, request, *args, **kwargs):
        if int(kwargs["pk"]) != int(self.request.user.pk):
            raise PermissionDenied
        return super().update(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        if int(kwargs["pk"]) != int(self.request.user.pk):
            raise PermissionDenied
        return super().destroy(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        if int(kwargs["pk"]) != int(self.request.user.pk):
            raise PermissionDenied
        return super().retrieve(request, args, kwargs)
