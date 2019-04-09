from django.contrib import admin
from .models import Transactions


class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'user', 'type', 'method', 'category')
    list_display = ('user', 'name', 'amount')


# Register your models here.
admin.site.register(Transactions, TransactionAdmin)
