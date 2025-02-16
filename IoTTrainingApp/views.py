# IoTTrainingApp/views.py
import os
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_absolute_error, mean_squared_error, f1_score
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import TrainedModel
from .serializers import TrainedModelSerializer
# import requests

@api_view(['GET'])
def train_model(request, parameter_type):
    # Load dataset
    csv_file=os.path.join(settings.MEDIA_ROOT, 'dataset\All_Attacks.csv')
    dataset = pd.read_csv(csv_file, sep=';')
    X = dataset.drop('label', axis=1)
    y = dataset['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Configure hyperparameters based on parameter_type
    if parameter_type == 0:
        params = {'n_estimators': 100, 'max_features': 'sqrt', 'max_depth': 6, 'max_leaf_nodes': 6}
    elif parameter_type == 1:
        params = {'n_estimators': 50, 'max_features': 'log2', 'max_depth': 3, 'max_leaf_nodes': 3}
    elif parameter_type == 2:
        params = {'n_estimators': 100, 'max_features': 'log2', 'max_depth': 3, 'max_leaf_nodes': 6}
    else:
        return Response({"error": "Invalid parameter type"}, status=400)
    
    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'mae': mean_absolute_error(y_test, y_pred),
        'mse': mean_squared_error(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    # Save model
    model_path = os.path.join(settings.MEDIA_ROOT, 'models', f'model_type_{parameter_type}.pkl')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save to database
    trained_model = TrainedModel.objects.create(
        parameter_type=parameter_type,
        model_file=f'models/model_type_{parameter_type}.pkl',
        **metrics
    )
    
    return Response(TrainedModelSerializer(trained_model).data)
