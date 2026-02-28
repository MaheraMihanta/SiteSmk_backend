from django.contrib import admin

from .models import CheckInOut, DamagePhoto, Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'customer', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date')
    search_fields = ('vehicle__plate_number', 'customer__username')


@admin.register(CheckInOut)
class CheckInOutAdmin(admin.ModelAdmin):
    list_display = ('rental', 'kind', 'created_at', 'fuel_level', 'mileage')
    list_filter = ('kind',)


@admin.register(DamagePhoto)
class DamagePhotoAdmin(admin.ModelAdmin):
    list_display = ('check_in_out', 'created_at', 'description')
