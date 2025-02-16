# IoTTrainingApp/admin.py
from django.contrib import admin
from .models import TrainedModel

@admin.register(TrainedModel)
class TrainedModelAdmin(admin.ModelAdmin):
    list_display = ('parameter_type', 'accuracy', 'precision', 'recall', 'f1_score', 'created_at')
    list_filter = ('parameter_type', 'created_at')
    readonly_fields = ('accuracy', 'precision', 'recall', 'mae', 'mse', 'f1_score', 'created_at')
    ordering = ('-created_at',)