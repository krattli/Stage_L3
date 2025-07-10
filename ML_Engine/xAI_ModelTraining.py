from .dataPreparation import prepData
from .models import AvailableModels, ModelType, MODEL_MAP

import os
from django.conf import settings
from typing import Tuple, List, Dict, Any, cast

import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import seaborn as sns
import base64
import io

def getModelPredictions(model_name:str) -> Tuple[ np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, ModelType, List[str]]:
    model = getModelByName(model_name)
    path = os.path.join(settings.BASE_DIR, 'static', 'data', 'dataset.csv')
    X_train, X_test, y_train, y_test, features_names = prepData(path)
    model.fit(X_train, y_train)
    y_pred = np.asarray(model.predict(X_test)) # Obligé de faire un cast ici pour le typage statique
    return X_train, X_test, y_train, y_test, y_pred, model, features_names

def getReportFromData(y_test:np.ndarray, y_pred:np.ndarray, model_name:str) -> Tuple[str, Dict[str, Any]]:
    confusionMatrixImg = getConfusionMatrixImage(y_test, y_pred, model_name) 
    report = cast(Dict[str,Any], classification_report(y_test, y_pred, output_dict=True))
    newLabels = { "0": "E+P+", "1": "E+P-", "2": "E-P+", "3": "E-P-" }
    usefullStats = changereportLabel(report, newLabels )
    return confusionMatrixImg, usefullStats

def getConfusionMatrixImage(y_test:np.ndarray, y_pred:np.ndarray, model_name:str) ->str:
    matrix = confusion_matrix(y_test, y_pred)
    matplotlib.use("Agg") # lorsqu'une image est générée avec plot(), elle est juste chargée en mémoire et pas affichée directement à l'écran
    plt.figure(figsize=(6, 5))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues')
    plt.title(f"Matrice de Confusion du modèle {model_name}")
    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    confusionMatrixImg_png = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return confusionMatrixImg_png

def getModelByName(model_name:str) -> ModelType:
    #print("on cherche le modèle : "+ model_name)
    #print("Available:", [m.name for m in AvailableModels.BlackboxModels])
    try:
        return MODEL_MAP[AvailableModels[model_name]]
    except KeyError:
        raise

def changereportLabel(report: Dict[str, Any], newLabels: Dict[str, str]) -> Dict[str, Any]:
    renamed_report = {}
    for key, val in report.items():
        if key in newLabels:
            renamed_report[newLabels[key]] = val
        else:
            renamed_report[key] = val
    return renamed_report
