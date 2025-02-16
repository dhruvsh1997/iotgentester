# IoTTestingApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generator_page, name='generator_page'),
    path('generate-data/', views.generate_data, name='generate_data'),
    path('test/', views.tester_page, name='tester_page'),
]
