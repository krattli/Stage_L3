from lime.lime_tabular import LimeTabularExplainer
import shap
from alibi.explainers import AnchorTabular
from sklearn.inspection import permutation_importance
import numpy as np
from .xAI_ModelTraining import getModelPredictions

def getExplanation(model_name, method):
    X_train, X_test, y_train, y_test, y_pred, model, feature_names = getModelPredictions(model_name)

    if method == "LIME":
        return explain_with_lime(model, X_train, X_test, feature_names, ["E+P+", "E+P-", "E-P+", "E-P-"])
    elif method == "SHAP":
        return explain_with_shap(model, X_train)
    elif method == "ANCHOR":
        return explain_with_anchor(model, X_train, feature_names)
    elif method == "PFI":
        return explain_with_pfi(model, X_test, y_test)
    else:
        raise ValueError("Méthode XAI non supportée")

def explain_with_lime(model, X_train, X_test, feature_names, class_names):
    explainer = LimeTabularExplainer(
        training_data=np.array(X_train),
        feature_names=feature_names,
        class_names=class_names,
        mode="classification"
    )
    explanation = explainer.explain_instance(X_test[0], model.predict_proba)
    return explanation.as_list()

def explain_with_shap(model, X_train):
    explainer = shap.Explainer(model.predict, X_train)
    shap_values = explainer(X_train[:10])
    return shap_values

def explain_with_anchor(model, X_train, feature_names):
    explainer = AnchorTabular(predictor=model.predict, feature_names=feature_names)
    explainer.fit(X_train, disc_perc=(25, 50, 75))
    explanation = explainer.explain(X_train[0])
    return explanation.data['anchor'], explanation.data['precision'], explanation.data['coverage']

def explain_with_pfi(model, X_test, y_test):
    results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
    if isinstance(results, dict):
        first_key = next(iter(results))
        result_bunch = results[first_key]
    else:
        result_bunch = results
    return result_bunch.importances_mean, result_bunch.importances_std

if __name__ == "__main__":
    print("hello world")
