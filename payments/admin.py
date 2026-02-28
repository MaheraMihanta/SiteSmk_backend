from django.contrib import admin

from .models import Invoice, Payment, Quote


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'method', 'status', 'paid_at', 'payer', 'received_by')
    list_filter = ('method', 'status')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'issue_date', 'status', 'total')
    list_filter = ('status',)
    search_fields = ('number',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('number', 'issue_date', 'status', 'total')
    list_filter = ('status',)
    search_fields = ('number',)
