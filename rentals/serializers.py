from rest_framework import serializers

from fleet.serializers import VehicleSerializer

from .models import CheckInOut, DamagePhoto, Rental


class RentalSerializer(serializers.ModelSerializer):
    vehicle_detail = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = Rental
        fields = [
            'id',
            'vehicle',
            'vehicle_detail',
            'customer',
            'created_by',
            'start_date',
            'end_date',
            'actual_return_date',
            'status',
            'daily_rate_at_booking',
            'deposit_amount',
            'notes',
            'created_at',
        ]
        read_only_fields = ['created_by', 'created_at']
        extra_kwargs = {'customer': {'required': False}}


class CheckInOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInOut
        fields = '__all__'


class DamagePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DamagePhoto
        fields = '__all__'
