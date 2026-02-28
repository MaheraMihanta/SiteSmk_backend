from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import UserRole
from accounts.permissions import IsOwnerOrEmployee

from .models import MaintenanceEvent, Vehicle
from .serializers import MaintenanceEventSerializer, VehicleSerializer


class VehicleAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in (UserRole.OWNER, UserRole.EMPLOYEE)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('id')
    serializer_class = VehicleSerializer
    permission_classes = [VehicleAccessPermission]


class MaintenanceEventViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceEvent.objects.all().order_by('-date')
    serializer_class = MaintenanceEventSerializer
    permission_classes = [IsOwnerOrEmployee]
