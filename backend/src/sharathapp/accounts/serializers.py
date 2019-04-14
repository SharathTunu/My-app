from rest_framework.serializers import *

from .models import *


class UserSerializer(ModelSerializer):
    """
    A serializer for our user profile objects.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
