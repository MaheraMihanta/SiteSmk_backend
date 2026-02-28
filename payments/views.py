from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

from accounts.models import UserRole

from documents.pdf import generate_invoice_pdf
from .models import Invoice, Payment, Quote
from .serializers import InvoiceSerializer, PaymentSerializer, QuoteSerializer


class CustomerReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == UserRole.CUSTOMER and request.method not in SAFE_METHODS:
            return False
        return True


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, CustomerReadOnly]

    def get_queryset(self):
        qs = Payment.objects.select_related('rental', 'payer').order_by('-paid_at')
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            return qs.filter(payer=user)
        return qs

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            serializer.save(payer=user)
        else:
            serializer.save(received_by=user)


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, CustomerReadOnly]

    def get_queryset(self):
        qs = Invoice.objects.select_related('rental').order_by('-issue_date')
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            return qs.filter(rental__customer=user)
        return qs

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        invoice = self.get_object()
        generate_invoice_pdf(invoice)
        serializer = self.get_serializer(invoice)
        return Response(serializer.data)


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated, CustomerReadOnly]

    def get_queryset(self):
        qs = Quote.objects.select_related('rental').order_by('-issue_date')
        user = self.request.user
        if user.role == UserRole.CUSTOMER:
            return qs.filter(rental__customer=user)
        return qs
