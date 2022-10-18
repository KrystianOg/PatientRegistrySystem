from rest_framework import viewsets


from .serializers import (
    AppointmentSerializer,
    RequestSerializer,
    UserSerializer,
)
from .models import Appointment, Request, User
from .mixins import ObjectPermissionMixin

"""
CHEAT SHEET
get -> list -> Queryset
get -> retrieve -> Instance Detail
post -> create -> New Instance
put -> Full Update
patch -> Partial Update (or Full)
delete -> destroy
"""


class AppointmentViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_serializer_context(self):
        self.request.data["doctor"] = self.request.user.pk


class RequestViewSet(ObjectPermissionMixin, viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    def get_serializer_context(self):
        self.request.data["patient"] = self.request.user.pk
        pass


# maybe without CreateModelMixin but for sure? (need to create user during signup process)
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
