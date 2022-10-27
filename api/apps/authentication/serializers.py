from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.apps.authentication.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        # ...

        return token


class RegisterPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password

        """
        (password, password2) = (value, self.context.get("password2"))
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        return value

    def create(self, validated_data):
        patient = User.objects.create_user(**validated_data)
        return patient


class RegisterDoctorSerializer(RegisterPatientSerializer):
    def create(self, validated_data):
        doctor = User.objects.create_doctor(**validated_data)
        return doctor


class ChangePasswordSerializer(serializers.Serializer):  # noqa
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context.get("request").user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"message": "wrong old password"})

        if attrs["new_password"] == attrs["old_password"]:
            raise serializers.ValidationError(
                {"message": "new password must be different from old password"}
            )
        return attrs


# TODO: add more serializers for views


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username"]
        read_only_fields = ["id", "email"]

    def update(self, instance, validated_data):
        if self.context.get("request").user.pk != instance.pk:
            raise serializers.ValidationError("Trying to change different account")
        return super().update(instance, validated_data)


class DetailedUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "types",
            "with_google",
            "vacation_mode",
            "prefer_dark_mode",
            "doctor_changes_appointment",
            "doctor_changes_appointment",
            "doctor_accepts_appointment",
        ]
        read_only_fields = UserSerializer.Meta.read_only_fields + ["with_google", "types"]
