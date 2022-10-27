from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.response import Response

from .serializers import (
    AppointmentSerializer,
    RequestSerializer,
    GetRequestSerializer,
    GetAppointmentSerializer,
)
from .models import Appointment, Request, User
from ..authentication.serializers import UserSerializer


# from .mixins import ObjectPermissionMixin


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

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
        request.data["doctor"] = request.user.pk
        instance = super().create(request, *args, **kwargs)
        req = request.data.get("request")
        Request.objects.get(pk=req).delete()
        return instance

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GetAppointmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetAppointmentSerializer(instance)
        return Response(serializer.data)


class RequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = GetRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetRequestSerializer(instance)
        return Response(serializer.data)


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
