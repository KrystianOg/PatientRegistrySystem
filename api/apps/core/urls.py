from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, RequestViewSet, UserViewSet


router = DefaultRouter()
router.register("appointments", AppointmentViewSet, basename="appointments")
router.register("requests", RequestViewSet, basename="requests")
router.register("users", UserViewSet, basename="users")


urlpatterns = router.urls
