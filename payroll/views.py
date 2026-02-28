from rest_framework import viewsets

from accounts.permissions import IsOwner

from .models import PayrollPayment
from .serializers import PayrollPaymentSerializer


class PayrollPaymentViewSet(viewsets.ModelViewSet):
    queryset = PayrollPayment.objects.select_related('employee').order_by('-period_start')
    serializer_class = PayrollPaymentSerializer
    permission_classes = [IsOwner]
