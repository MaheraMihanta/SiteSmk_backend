from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PayrollPaymentViewSet

router = DefaultRouter()
router.register(r'payrolls', PayrollPaymentViewSet, basename='payrolls')

urlpatterns = [
    path('', include(router.urls)),
]
