from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'username',)
    list_display = ('first_name', 'last_name', 'username',)


# Register your models here.
admin.site.register(User, UserAdmin)
