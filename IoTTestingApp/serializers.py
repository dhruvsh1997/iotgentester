# IoTTestingApp/serializers.py
from rest_framework import serializers
from .models import IoTGeneratedData

class IoTGeneratedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTGeneratedData
        fields = '__all__'