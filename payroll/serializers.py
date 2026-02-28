from rest_framework import serializers

from .models import PayrollPayment


class PayrollPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPayment
        fields = '__all__'
