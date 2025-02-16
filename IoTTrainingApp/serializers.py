# IoTTrainingApp/serializers.py
from rest_framework import serializers
from .models import TrainedModel

class TrainedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedModel
        fields = '__all__'
        read_only_fields = ('model_file', 'accuracy', 'precision', 'recall', 'mae', 'mse', 'f1_score', 'created_at')
