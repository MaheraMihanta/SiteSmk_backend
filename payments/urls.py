from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, PaymentViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'quotes', QuoteViewSet, basename='quotes')

urlpatterns = [
    path('', include(router.urls)),
]
