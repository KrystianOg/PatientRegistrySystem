from rest_framework import viewsets, status
from rest_framework import exceptions
from rest_framework.response import Response

from .serializers import AppointmentSerializer, RequestSerializer, UserSerializer, AppointmentPatientSerializer
from .models import Appointment, Request, User
from django.db.models import Q


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
    lookup_field = 'pk'     # default

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.PermissionDenied
        if user.UserType == User.UserType.PATIENT:
            queryset = Appointment.objects.filter(patient=user)
        elif user.UserType == User.UserType.DOCTOR:
            queryset = Appointment.objects.filter(doctor=user)
        else:
            queryset = Appointment.objects.all()
        return queryset

    def get_serializer_class(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.PermissionDenied   # will be changed in Permission issue
        if user.UserType == User.UserType.PATIENT:
            serializer_class = AppointmentPatientSerializer
        else:
            serializer_class = AppointmentSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):     # redundant using separate serializer above but idk
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
            raise exceptions.PermissionDenied
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
    serializer_class = UserSerializer
    lookup_field = 'pk'     # default

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise exceptions.PermissionDenied
        if user.UserType == User.UserType.PATIENT:
            queryset = User.objects.get(email=user.email)
        elif user.UserType == User.UserType.DOCTOR:
            criterion1 = Q(type=User.UserType.PATIENT)
            criterion2 = Q(type=User.UserType.DOCTOR)
            queryset = User.objects.filter(criterion1 & criterion2)
        else:
            queryset = User.objects.all()
        return queryset

