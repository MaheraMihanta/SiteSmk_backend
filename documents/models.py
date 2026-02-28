from django.db import models

from rentals.models import Rental


class ContractStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Brouillon'
    ISSUED = 'ISSUED', 'Émis'
    SIGNED = 'SIGNED', 'Signé'


class Contract(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.SET_NULL, null=True, blank=True, related_name='contracts')
    number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    status = models.CharField(max_length=20, choices=ContractStatus.choices, default=ContractStatus.DRAFT)
    pdf_file = models.FileField(upload_to='contracts/', null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.number
