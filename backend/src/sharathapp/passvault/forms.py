from django.forms import *
from .models import PasswordVault


class PasswordVaultForm(ModelForm):

    class Meta:
        model = PasswordVault
        fields = '__all__'

    def save(self, commit=True):
        instance = super(PasswordVaultForm, self).save(commit=False)
        instance.save()

        return instance


class ShowPasswordForm(Form):

    application = CharField(max_length=100)
    username = CharField(max_length=100)
    password = CharField(max_length=1000)

