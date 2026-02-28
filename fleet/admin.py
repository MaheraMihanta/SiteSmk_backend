from django.contrib import admin

from .models import MaintenanceEvent, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'type', 'make', 'model', 'year', 'status', 'daily_rate')
    search_fields = ('plate_number', 'make', 'model')
    list_filter = ('type', 'status')


@admin.register(MaintenanceEvent)
class MaintenanceEventAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'cost', 'next_due_date')
    list_filter = ('date',)
