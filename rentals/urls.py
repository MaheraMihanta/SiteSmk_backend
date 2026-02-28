from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CheckInOutViewSet, DamagePhotoViewSet, RentalViewSet

router = DefaultRouter()
router.register(r'rentals', RentalViewSet, basename='rentals')
router.register(r'checks', CheckInOutViewSet, basename='checks')
router.register(r'damages', DamagePhotoViewSet, basename='damages')

urlpatterns = [
    path('', include(router.urls)),
]
