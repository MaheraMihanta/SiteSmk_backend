from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'issue_date', 'status')
    list_filter = ('status',)
    search_fields = ('number',)
