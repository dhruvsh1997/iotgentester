# IoTTestingApp/views.py
import json
import pickle
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import IoTGeneratedData
from .utils.iot_generator import IoTDataGenerator
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_absolute_error, mean_squared_error, f1_score
from django.conf import settings
import os

def generator_page(request):
    return render(request, 'IoTTestingApp/generator.html')

def generate_data(request):
    if request.method == 'POST':
        num_rows = int(request.POST.get('num_rows', 10))
        generator = IoTDataGenerator()
        
        generated_data = []
        for _ in range(num_rows):
            row = generator.generate_single_row()
            generated_data.append(row)
            
            # Save to database
            IoTGeneratedData.objects.create(
                second=row[0], src=row[1], dst=row[2], packetcount=row[3],
                src_ratio=row[4], dst_ratio=row[5], src_duration_ratio=row[6],
                dst_duration_ratio=row[7], TotalPacketDuration=row[8],
                TotalPacketLenght=row[9], src_packet_ratio=row[10],
                dst_packet_ratio=row[11], DioCount=row[12], DisCount=row[13],
                DaoCount=row[14], OtherMsg=row[15], label=row[16]
            )
        
        df = pd.DataFrame(generated_data, columns=[
            'second', 'src', 'dst', 'packetcount', 'src_ratio', 'dst_ratio',
            'src_duration_ratio', 'dst_duration_ratio', 'TotalPacketDuration',
            'TotalPacketLenght', 'src_packet_ratio', 'dst_packet_ratio',
            'DioCount', 'DisCount', 'DaoCount', 'OtherMsg', 'label'
        ])
        
        return JsonResponse({
            'data': df.to_dict('records'),
            'columns': df.columns.tolist()
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def tester_page(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', '[]'))
        df = pd.DataFrame(data)
        
        # Load the latest model
        model_path = os.path.join(settings.MEDIA_ROOT, 'models')
        latest_model = max([f for f in os.listdir(model_path) if f.endswith('.pkl')])
        
        with open(os.path.join(model_path, latest_model), 'rb') as f:
            model = pickle.load(f)
        
        # Prepare data
        X = df.drop('label', axis=1)
        y = df['label']
        
        # Make predictions
        y_pred_converted = model.predict(X)
        min_val = min(y_pred_converted)
        y_pred = [0 if x == min_val else 1 for x in y_pred_converted]
        # Calculate metrics
        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, average='weighted'),
            'recall': recall_score(y, y_pred, average='weighted'),
            'mae': mean_absolute_error(y, y_pred),
            'mse': mean_squared_error(y, y_pred),
            'f1_score': f1_score(y, y_pred, average='weighted')
        }
        
        # Combine input and predictions
        df['predicted_label'] = y_pred
        
        return render(request, 'IoTTestingApp/tester.html', {
            'data': df.to_dict('records'),
            'metrics': metrics
        })
    
    return redirect('generator_page')