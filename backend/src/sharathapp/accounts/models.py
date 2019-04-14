from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        Group, GroupManager, PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .fields import PhoneNumberField
from common_methods import *

from datetime import datetime
from django_pandas.io import read_frame


class UserManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, username, first_name, last_name, password=None, email=None):
        """Creates a new user profile."""

        if not username:
            raise ValueError('The given username must be set')

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, first_name, last_name, password, email=None):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(username, first_name, last_name, password, email)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    first_name = models.TextField(db_index=True)
    last_name = models.TextField(db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    username = models.CharField(max_length=255, unique=True, validators=[RegexValidator(r'^[\w\d@\.]+$')])
    
    phone_number = PhoneNumberField(db_index=True, null=True, default=None)

    registration_date = models.DateTimeField(auto_now_add=True, null=True)

    objects = UserManager()
    search_fields = ('name',)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def sagroups(self):
        """Returning the tags for fh groups that the user belongs to"""
        sagroups = []
        # Get all groups
        if self.id:
            groups = self.groups.all()
            if groups:
                # Get fh groups tags
                for group in groups:
                    if hasattr(group, 'sagroup'):
                        sagroups.append(group.sagroup.tag)

        return sagroups

    def __str__(self):
        return self.username
    
    @property
    def transactions_as_df(self):
        return read_frame(self.financialtransaction_set.all())
    
    def export_to_excel(self, report_df=pd.DataFrame()):        
        response = dict()
        transactions = self.transactions_as_df
        response["Transactions"] = transactions
        response["Summary"] = dataframe_summary(transactions)
        return response


class SAGroup(Group):
    """Extending the default django groups"""

    tag = models.CharField(unique=True, max_length=250)

    SA_AGENT = 'Trusted Friend'

    class Meta:
        verbose_name = _('SA Group')
        verbose_name_plural = _('SA Groups')
