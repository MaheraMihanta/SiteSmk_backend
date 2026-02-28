from django.db import models


class VehicleType(models.TextChoices):
    CAR = 'CAR', 'Voiture'
    MOTORCYCLE = 'MOTORCYCLE', 'Moto'


class VehicleStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Disponible'
    RENTED = 'RENTED', 'Loué'
    MAINTENANCE = 'MAINTENANCE', 'Maintenance'
    INACTIVE = 'INACTIVE', 'Inactif'


class Vehicle(models.Model):
    type = models.CharField(max_length=20, choices=VehicleType.choices)
    status = models.CharField(max_length=20, choices=VehicleStatus.choices, default=VehicleStatus.AVAILABLE)
    plate_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30, blank=True)
    vin = models.CharField(max_length=50, blank=True)
    mileage = models.PositiveIntegerField(default=0)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.plate_number} - {self.make} {self.model}"


class MaintenanceEvent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_events')
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    next_due_date = models.DateField(null=True, blank=True)
    odometer = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.vehicle.plate_number} - {self.date}"
