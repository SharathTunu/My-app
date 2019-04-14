from django.forms import *
from .models import *
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'

    def save(self, commit=True):
        instance = super(ResumeForm, self).save(commit=False)
        return instance