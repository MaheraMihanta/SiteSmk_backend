from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomerProfile, EmployeeProfile, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {'fields': ('display_name', 'role', 'phone', 'address')}),
    )
    list_display = ('username', 'display_name', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'base_salary', 'hire_date')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'driver_license_number', 'driver_license_expiry')
