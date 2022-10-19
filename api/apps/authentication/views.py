from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from api.apps.authentication.serializers import (
    MyTokenObtainPairSerializer,
    RegisterPatientSerializer,
    ChangePasswordSerializer,
    RegisterDoctorSerializer,
)


# for jwt tokens
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


# TODO: remove response data when 201
class SignUpPatientViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterPatientSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {
            "password2": self.request.data.get("password2"),
        }


class SignUpDoctorViewSet(SignUpPatientViewSet):
    serializer_class = RegisterDoctorSerializer
    permission_classes = [AllowAny]


class ChangePasswordViewSet(UpdateModelMixin, GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
