from django.db import models
from django.utils.translation import ugettext_lazy as _


class PhoneNumberField(models.TextField):
    description = "Phone number fields to accept value in +x(xxx)-xxx-xxxx format"

    def __init__(self, *args, **kwargs):
        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value

        return '+%s(%s)-%s-%s' % (value[:1], value[1:4], value[4:7], value[7:])

    def to_python(self, value):
        import re
        from django.core.exceptions import ValidationError

        if value is None:
            return value

        cleaned_value = re.sub(r"\+|-|\(|\)", "", value)

        # 11 digits only
        if not re.search(r"^\d{11}$", cleaned_value):
            raise ValidationError(
                _('Ensure this field has right phone number value. Expected format e.g. +1(234)-567-8899')
            )

        return cleaned_value
