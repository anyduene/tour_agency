from rest_framework import serializers
from api.models import Transport


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = '__all__'