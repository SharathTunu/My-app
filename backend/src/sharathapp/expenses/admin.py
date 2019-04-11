from django.contrib import admin
from .models import FinancialTransaction


class FinancialTransactionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'user', 'type', 'method', 'category')
    list_display = ('user', 'name', 'amount')


# Register your models here.
admin.site.register(FinancialTransaction, FinancialTransactionAdmin)
