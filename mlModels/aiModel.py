from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

from mlModels.dataPreparation import prepData

import os
from django.conf import settings

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

BLACKBOX_MODELS = {
    "Decision Tree": DecisionTreeClassifier(),
    "Logistic Regression": LogisticRegression(),
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier(),
}

WHITEBOX_MODELS = {
    "Random Forest": RandomForestClassifier(),
    "Bagging": BaggingClassifier(),
    "Extra Trees": ExtraTreesClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "MLP": MLPClassifier()
}

AVAILABLE_MODELS = {**WHITEBOX_MODELS, **BLACKBOX_MODELS}

"""
    Prends un String du nom de modèle et montre la matrice de confusion que ce modèle produit sur les données d'entrainement statiques
"""
def plotConfusionMatrix(MLmodel):
    if MLmodel in AVAILABLE_MODELS:
        model = AVAILABLE_MODELS[MLmodel]
        path = os.path.join(settings.BASE_DIR, 'static', 'data', 'dataset.csv')
        X_train, X_test, y_train, y_test = prepData(path)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        plt.figure(figsize=(8, 6))
        plt.title(f"Matrice de Confusion de : {MLmodel}")
        plt.imshow(confusion_matrix(y_test, y_pred), cmap='Blues', interpolation='nearest')
        plt.colorbar()
        plt.xlabel('Prédictions')
        plt.ylabel('Réelles')
        plt.xticks([0, 1, 2, 3], ['E+P+', 'E+P-', 'E-P+', 'E-P-'])
        plt.yticks([0, 1, 2, 3], ['E+P+', 'E+P-', 'E-P+', 'E-P-'])
        plt.show()
    else:
        print(f"Le modèle d'IA '{MLmodel}' n'est pas encore disponible. Veuillez choisir parmi les modèles suivants : {list(AVAILABLE_MODELS.keys())}")

if __name__ == "__main__":
    for model in AVAILABLE_MODELS.values():
        plotConfusionMatrix(model)
