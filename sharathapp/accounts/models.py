from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from .fields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    """
    Create a custom user using django base user model.
    """
    email = models.EmailField(unique=True)

    first_name = models.TextField(db_index=True)
    last_name = models.TextField(db_index=True)
    job_title = models.TextField(db_index=True, null=True, default=None)

    username = models.CharField(max_length=255, unique=True, validators=[RegexValidator(r'^[\w\d@\.]+$')])

    phone_number = PhoneNumberField(db_index=True, null=True, default=None)

    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

