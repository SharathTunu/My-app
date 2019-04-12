import pandas as pd
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from .models import User
from io import BytesIO, StringIO


class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'username',)
    list_display = ('first_name', 'last_name', 'username',)
    actions = ['export_to_csv','export_report_to_excel']

    def export_to_excel(self, request, queryset):
        for report in queryset:
            try:
                sio = BytesIO()
                writer = pd.ExcelWriter(sio, engine='xlsxwriter')
                for k, v in report.export_to_excel().items():
                    keep_index = k != "Loans" # Drops df index for loans.
                    v.to_excel(writer, k, index=keep_index)
                    
                writer.save()
                sio.seek(0)
                workbook = sio.read()

                response = HttpResponse(workbook, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")  
                response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(report.file_name)
                return response
            except:
                raise
    export_to_excel.short_description = "Export the report (for only one user) to excel"
    
    def export_to_csv(self, request, queryset):
        for user in queryset:
            try:
                expenses = user.transactions_as_df
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename={}.csv'.format(user.full_name)

                expenses.to_csv(path_or_buf=response, index =False)
                return response
            except:
                raise
    export_to_csv.short_description = "Export the report (for only one user) to csv"


# Register your models here.
admin.site.register(User, UserAdmin)
