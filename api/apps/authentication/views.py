from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from api import settings
from api.apps.authentication.models import User

from api.apps.authentication.serializers import (
    MyTokenObtainPairSerializer,
    RegisterPatientSerializer,
    ChangePasswordSerializer,
    RegisterDoctorSerializer,
)

from google.oauth2 import id_token
from google.auth.transport import requests


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token = User.objects.get(email=request.data.get("email")).get_token()
        return Response(token, status=status.HTTP_201_CREATED)


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


class GoogleSignInView(RetrieveModelMixin, GenericViewSet):
    def retrieve(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")

        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID, clock_skew_in_seconds=4
            )
            email = idinfo["email"]
            given_name = idinfo["given_name"]
            family_name = idinfo["family_name"]

            if User.objects.filter(email=email).exists():
                token = User.objects.get(email=email).get_token()
                return Response(token, status=status.HTTP_200_OK)
            else:
                user = User.objects.create_user(
                    email=email, first_name=given_name, last_name=family_name
                )
                user.save()
                return Response(user.get_token(), status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_403_FORBIDDEN)
