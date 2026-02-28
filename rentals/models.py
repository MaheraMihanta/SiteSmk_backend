from django.conf import settings
from django.db import models

from fleet.models import Vehicle


class RentalStatus(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmée'
    ACTIVE = 'ACTIVE', 'En cours'
    COMPLETED = 'COMPLETED', 'Terminée'
    CANCELED = 'CANCELED', 'Annulée'
    OVERDUE = 'OVERDUE', 'En retard'


class Rental(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='rentals')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='rentals')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_rentals'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RentalStatus.choices, default=RentalStatus.PENDING)
    daily_rate_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.vehicle.plate_number} - {self.start_date} -> {self.end_date}"


class CheckInOutKind(models.TextChoices):
    CHECK_OUT = 'CHECK_OUT', 'Sortie'
    CHECK_IN = 'CHECK_IN', 'Retour'


class CheckInOut(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='checks')
    kind = models.CharField(max_length=20, choices=CheckInOutKind.choices)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fuel_level = models.PositiveIntegerField(default=100)
    mileage = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.rental.id} - {self.kind}"


def damage_photo_path(instance, filename: str) -> str:
    return f"rentals/{instance.check_in_out.rental_id}/damages/{filename}"


class DamagePhoto(models.Model):
    check_in_out = models.ForeignKey(CheckInOut, on_delete=models.CASCADE, related_name='damage_photos')
    image = models.ImageField(upload_to=damage_photo_path)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
