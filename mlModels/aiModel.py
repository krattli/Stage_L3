from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from dataPreparation import prepData

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

WHITEBOX_MODELS = {
    "Decision Tree": DecisionTreeClassifier(),
    "Logistic Regression": LogisticRegression(),
    "Naive Bayes": GaussianNB(),
    "KNN": KNeighborsClassifier()
}

BLACKBOX_MODELS = {
    "Random Forest": RandomForestClassifier(),
    "Bagging": BaggingClassifier(),
    "Extra Trees": ExtraTreesClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "MLP": MLPClassifier()
}

def plotConfusionMatrix(model):
    X_train, X_test, y_train, y_test = prepData('../static/data/dataset.csv')
    # Entraînement du modèle
    model.fit(X_train, y_train)
    # Prédictions
    y_pred = model.predict(X_test)
    # Afficher les résultats
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    # On va afficher la matrice de confusion de façon graphique
    plt.figure(figsize=(8, 6))
    plt.title(f"Matrice de Confusion de :{type(model)}")
    plt.imshow(confusion_matrix(y_test, y_pred), cmap='Blues', interpolation='nearest')
    plt.colorbar()
    plt.xlabel('Prédictions')
    plt.ylabel('Réelles')
    plt.xticks([0, 1, 2, 3], ['E+P+', 'E+P-', 'E-P+', 'E-P-'])
    plt.yticks([0, 1, 2, 3], ['E+P+', 'E+P-', 'E-P+', 'E-P-'])
    plt.show()

if __name__ == "__main__":
    for model in WHITEBOX_MODELS.values():
        plotConfusionMatrix(model)
    for model in BLACKBOX_MODELS.values():
        plotConfusionMatrix(model)
