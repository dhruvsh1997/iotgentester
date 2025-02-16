# IoTTrainingApp/models.py
from django.db import models

class TrainedModel(models.Model):
    parameter_type = models.IntegerField(choices=[(0, 'Type 0'), (1, 'Type 1'), (2, 'Type 2')])
    model_file = models.FileField(upload_to='models/')
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    mae = models.FloatField()
    mse = models.FloatField()
    f1_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Model Type {self.parameter_type} - {self.created_at}"