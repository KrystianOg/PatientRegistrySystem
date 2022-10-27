from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyTokenObtainPairView,
    ChangePasswordViewSet,
    GoogleSignInView,
    SignUpDoctorViewSet,
    SignUpPatientViewSet,
    UserDetailView,
)

auth_urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),  # to sign in
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignUpPatientViewSet.as_view({"post": "create"}), name="signup"),  # to sign up
    path(
        "signup/doctor/", SignUpDoctorViewSet.as_view({"post": "create"}), name="signup-doctor"
    ),  # to sign up
    path(
        "change-password/",
        ChangePasswordViewSet.as_view({"patch": "update"}),
        name="update_password",
    ),
    path("google/signin/", GoogleSignInView.as_view({"get": "retrieve"}), name="google_signin"),
    path(
        "user/<int:pk>/",
        UserDetailView.as_view(
            {"get": "retrieve", "patch": "partial_update", "put": "update", "delete": "destroy"}
        ),
        name="user_detail",
    ),
]

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    # TODO: add some user urls here
]
