from rest_framework import viewsets
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
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
