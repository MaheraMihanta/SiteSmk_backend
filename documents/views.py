from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsOwnerOrEmployee

from .models import Contract
from .pdf import generate_contract_pdf
from .serializers import ContractSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.select_related('rental').order_by('-issue_date')
    serializer_class = ContractSerializer
    permission_classes = [IsOwnerOrEmployee]

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        contract = self.get_object()
        generate_contract_pdf(contract)
        serializer = self.get_serializer(contract)
        return Response(serializer.data)
