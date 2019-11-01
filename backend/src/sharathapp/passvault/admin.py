from django.contrib import admin
from django.conf.urls import *
from django.utils.html import format_html
from django.urls import reverse
from .models import *
from django.template.response import TemplateResponse
from .forms import ShowPasswordForm


# Register your models here.
@admin.register(PasswordVault)
class PasswordVaultAdmin(admin.ModelAdmin):
    search_fields = ('application', 'username')
    ordering = ('application',)
    list_display = ('username', 'application', 'password', 'instance_actions',)

    def instance_actions(self, obj):
        print("instance_actions")
        return format_html(
            '<a class="button" href="{}">Show Password</a>&nbsp;',
            reverse('admin:showpass', kwargs={"id": obj.pk}),
        )

    instance_actions.short_description = 'Password Actions'
    instance_actions.allow_tags = True

    def get_queryset(self, request):
        qs = super(PasswordVaultAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_id=request.user.id)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/showpass/$',
                self.admin_site.admin_view(self.show_password),
                name='showpass',
            ),
        ]
        return custom_urls + urls

    def show_password(self, request, *args, **kwargs):
        instance = self.get_object(request, kwargs["id"])
        data = {
            'application': instance.application,
            'username': instance.username,
            'password': instance.decrypt
        }
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = ShowPasswordForm(data)
        context['account'] = self.get_object(request, kwargs["id"])
        context['title'] = "Show Password"
        # import pdb
        # pdb.set_trace()
        return TemplateResponse(request, 'admin/passvault/password_vault_action.html', context)


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    search_fields = ('user',)
    ordering = ('updated_at',)
    list_display = ('user', 'key', 'previous_key')
