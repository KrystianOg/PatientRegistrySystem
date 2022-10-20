from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        user_groups = set(user.groups.values_list("name", flat=True))

        if "Admin" in user_groups:
            queryset = Appointment.objects.all()
        elif "Doctor" in user_groups:
            queryset = Appointment.objects.filter(doctor=user)
        else:
            queryset = Appointment.objects.filter(patient=user)
        return queryset

    def create(self, request, *args, **kwargs):
        request_pk = request.data.get("request")
        request_obj = Request.objects.get(pk=request_pk)

        request.data["patient"] = request_obj.patient.pk
        request.data["symptoms"] = request_obj.symptoms
        request.data["comment"] = request_obj.comment
        request.data.pop("request")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        request_obj.delete()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
