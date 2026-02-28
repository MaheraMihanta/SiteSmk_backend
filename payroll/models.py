from django.conf import settings
from django.db import models


class PayrollStatus(models.TextChoices):
    PENDING = 'PENDING', 'En attente'
    PAID = 'PAID', 'Payé'
    CANCELED = 'CANCELED', 'Annulé'


class PayrollPayment(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='payrolls')
    period_start = models.DateField()
    period_end = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PayrollStatus.choices, default=PayrollStatus.PENDING)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.employee.username} - {self.period_start} -> {self.period_end}"
