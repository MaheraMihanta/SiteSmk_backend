from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsOwnerOrEmployee
from fleet.models import Vehicle, VehicleStatus
from payments.models import Payment, PaymentStatus
from rentals.models import Rental, RentalStatus


class DashboardSummaryView(APIView):
    permission_classes = [IsOwnerOrEmployee]

    def get(self, request):
        vehicles_total = Vehicle.objects.count()
        vehicles_available = Vehicle.objects.filter(status=VehicleStatus.AVAILABLE).count()
        rentals_active = Rental.objects.filter(status=RentalStatus.ACTIVE).count()
        rentals_overdue = Rental.objects.filter(status=RentalStatus.OVERDUE).count()
        revenue = (
            Payment.objects.filter(status=PaymentStatus.RECEIVED).aggregate(total=Sum('amount')).get('total') or 0
        )

        return Response(
            {
                'vehicles_total': vehicles_total,
                'vehicles_available': vehicles_available,
                'rentals_active': rentals_active,
                'rentals_overdue': rentals_overdue,
                'revenue': revenue,
            }
        )
