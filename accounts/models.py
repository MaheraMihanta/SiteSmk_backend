from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrateur'
    NATIONAL = 'NATIONAL', 'Bureau national'
    ENTITY = 'ENTITY', 'Entite locale'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.ENTITY)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    def is_admin_role(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_national_role(self) -> bool:
        return self.role == UserRole.NATIONAL

    def is_entity_role(self) -> bool:
        return self.role == UserRole.ENTITY

    def get_display_name(self) -> str:
        if self.display_name:
            return self.display_name
        full_name = self.get_full_name().strip()
        if full_name:
            return full_name
        return self.username


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    position = models.CharField(max_length=100, blank=True)
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hire_date = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.position})"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    driver_license_number = models.CharField(max_length=100, blank=True)
    driver_license_expiry = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.user.username

