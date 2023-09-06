from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    # Add additional fields for your custom User model here
    # For example:
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # You can also override or add methods specific to your custom User model
    # For example:
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # By default, the User model comes with the following fields:
    # username, email, first_name, last_name, password, groups, user_permissions,
    # is_staff, is_active, is_superuser, last_login, and date_joined.

    # If you need to customize the User model further, you can add fields,
    # properties, or methods as per your project requirements.
