from rest_framework.serializers import *

from .models import *


class TransactionSerializer(ModelSerializer):
    """
    A serializer for our transaction objects.
    """
    class Meta:
        model = FinancialTransaction
        fields = "__all__"

