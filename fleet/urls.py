from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MaintenanceEventViewSet, VehicleViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')
router.register(r'maintenance', MaintenanceEventViewSet, basename='maintenance')

urlpatterns = [
    path('', include(router.urls)),
]
