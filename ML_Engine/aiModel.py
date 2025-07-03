from .dataPreparation import prepData
from .models import AvailableModels

import os
from django.conf import settings

import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import base64
import io

def getReport(model):
    #model = getModelByName(model_name)
    predictions = getModelPredictions(model) # predictions[3]:y_train et predictions[4]:y_test
    confusionMatrixImg = getConfusionMatrixImage(predictions[3], predictions[4]) 
    report = classification_report(predictions[3], predictions[4], output_dict=True)
    newLabels = { "0": "E+P+", "1": "E+P-", "2": "E-P+", "3": "E-P-" }
    usefullStats = changereportLabel(report, newLabels )
    return confusionMatrixImg, usefullStats

def getConfusionMatrixImage(y_test, y_pred):
    matrix = confusion_matrix(y_test, y_pred)
    matplotlib.use("Agg") # lorsqu'une image est générée avec plot(), elle est juste chargée en mémoire et pas affichée directement à l'écran
    plt.figure(figsize=(6, 5))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues')
    plt.title("Matrice de Confusion")
    plt.xlabel("Prédictions")
    plt.ylabel("Vérités")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_png = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return image_png

def getModelByName(model_name):
    print("on cherche le modèle : "+ model_name)
    print("Available:", [m.name for m in AvailableModels.BlackboxModels])
    try:
        return AvailableModels.BlackboxModels[model_name].value
    except KeyError:
        try:
            return AvailableModels.WhiteBoxModels[model_name].value
        except Exception:
            raise

def getModelPredictions(model_name):
    model = getModelByName(model_name)
    path = os.path.join(settings.BASE_DIR, 'static', 'data', 'dataset.csv')
    X_train, X_test, y_train, y_test = prepData(path)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return X_train, X_test, y_train, y_test, y_pred

def changereportLabel(report, newLabels):
    renamed_report = {}
    for key, val in report.items():
        if key in newLabels:
            renamed_report[newLabels[key]] = val
        else:
            renamed_report[key] = val
    return renamed_report
