from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

from accounts.models import UserRole
from accounts.permissions import IsOwnerOrEmployee

from .models import CheckInOut, DamagePhoto, Rental, RentalStatus
from .serializers import CheckInOutSerializer, DamagePhotoSerializer, RentalSerializer


class RentalPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == UserRole.CUSTOMER and request.method not in SAFE_METHODS:
            return view.action == 'create'
        return True


class RentalViewSet(viewsets.ModelViewSet):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated, RentalPermission]

    def get_queryset(self):
        qs = Rental.objects.select_related('vehicle', 'customer').order_by('-created_at')
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            return qs.filter(customer=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            serializer.save(customer=user, created_by=user, status=RentalStatus.PENDING)
        else:
            serializer.save(created_by=user)


class CheckInOutViewSet(viewsets.ModelViewSet):
    queryset = CheckInOut.objects.select_related('rental').order_by('-created_at')
    serializer_class = CheckInOutSerializer
    permission_classes = [IsOwnerOrEmployee]


class DamagePhotoViewSet(viewsets.ModelViewSet):
    queryset = DamagePhoto.objects.select_related('check_in_out').order_by('-created_at')
    serializer_class = DamagePhotoSerializer
    permission_classes = [IsOwnerOrEmployee]
