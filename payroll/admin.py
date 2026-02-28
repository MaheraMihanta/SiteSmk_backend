from django.contrib import admin

from .models import PayrollPayment


@admin.register(PayrollPayment)
class PayrollPaymentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period_start', 'period_end', 'amount', 'status')
    list_filter = ('status',)
