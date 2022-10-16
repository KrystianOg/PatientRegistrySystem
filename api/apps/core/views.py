from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .serializers import AppointmentSerializer, RequestSerializer, UserSerializer
from .models import Appointment, Request, User


"""
CHEAT SHEET
get -> list -> Queryset
get -> retrieve -> Instance Detail
post -> create -> New Instance
put -> Full Update
patch -> Partial Update (or Full)
delete -> destroy
"""


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    lookup_field = 'pk'     # default

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied
        if user.UserType == User.UserType.PATIENT:
            queryset = Appointment.objects.filter(patient=user)
        elif user.UserType == User.UserType.DOCTOR:
            queryset = Appointment.objects.filter(doctor=user)
        else:
            queryset = Appointment.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous or user.UserType == User.UserType.PATIENT:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super().create(request, args, kwargs)


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    lookup_field = 'pk'     # default

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied
        if user.UserType == User.UserType.PATIENT:
            queryset = Request.objects.filter(patient=user)
        else:
            queryset = Request.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super().create(request, args, kwargs)


# maybe without CreateModelMixin but for sure? (need to create user during signup process)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'     # default

