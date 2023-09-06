from .models import CustomUser
from rest_framework import serializers

# Serializers define the API representation.
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
