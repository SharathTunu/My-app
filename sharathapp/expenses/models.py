from django.db import models

from accounts.models import User

from .constants import TransactionChoices as TC, TransactionVerboseNames as TVN
# Create your models here.


class Transactions(models.Model):
    """
    Create a custom user using django base user model.
    """
    user = models.ForeignKey(User)

    date = models.DateTimeField(auto_now_add=True, verbose_name=TVN.DATE)

    type = models.CharField(max_length=25, choices=TC.TYPE_CHOICES, default=TC.EXPENSE, verbose_name=TVN.TYPE)
    method = models.CharField(max_length=25, choices=TC.METHOD_CHOICES, default=TC.CREDIT_CARD, verbose_name=TVN.METHOD)
    name = models.CharField(max_length=100, verbose_name=TVN.NAME)
    category = models.CharField(max_length=100, default="Others", verbose_name=TVN.CATEGORY)
    amount = models.FloatField(default=0.00, verbose_name=TVN.AMOUNT)

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




