from django.conf import settings
from django.db import models

from rentals.models import Rental


class PaymentMethod(models.TextChoices):
    CASH = 'CASH', 'Espèces'
    CARD = 'CARD', 'Carte'
    TRANSFER = 'TRANSFER', 'Virement'
    MOBILE = 'MOBILE', 'Mobile money'


class PaymentStatus(models.TextChoices):
    RECEIVED = 'RECEIVED', 'Reçu'
    PENDING = 'PENDING', 'En attente'
    CANCELED = 'CANCELED', 'Annulé'


class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments_received'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.RECEIVED)
    paid_at = models.DateTimeField()
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Paiement {self.amount} ({self.method})"


class InvoiceStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Brouillon'
    ISSUED = 'ISSUED', 'Émise'
    PAID = 'PAID', 'Payée'
    CANCELED = 'CANCELED', 'Annulée'


class Invoice(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self) -> str:
        return self.number


class QuoteStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Brouillon'
    SENT = 'SENT', 'Envoyé'
    ACCEPTED = 'ACCEPTED', 'Accepté'
    REJECTED = 'REJECTED', 'Refusé'


class Quote(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotes')
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    valid_until = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=QuoteStatus.choices, default=QuoteStatus.DRAFT)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.number
