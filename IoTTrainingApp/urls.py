# IoTTrainingApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('train/<int:parameter_type>/', views.train_model, name='train_model'),
]
