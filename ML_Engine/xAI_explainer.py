from lime.lime_tabular import LimeTabularExplainer
from alibi.explainers import AnchorTabular
from sklearn.inspection import permutation_importance
from typing import List
import shap
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

from ML_Engine.models import ModelType
#from .xAI_ModelTraining import getModelPredictions

def getExplanation(X_train:np.ndarray, X_test:np.ndarray, y_test:np.ndarray, model:ModelType, feature_names:List[str], method:str) -> str:
    #X_train, X_test, y_train, y_test, y_pred, model, feature_names = getModelPredictions(model_name)

    if method == "LIME":
        raw =  explainWithLimeRaw(model, X_train, X_test, feature_names, ["E+P+", "E+P-", "E-P+", "E-P-"])
        return explainWithLimeView(raw)
    elif method == "SHAP":
        raw = explainWithShapRaw(model, X_train)
        return explainWithShapView(raw, feature_names)
    elif method == "ANCHOR":
        data, precision, coverage = explainWithAnchor(model, X_train, feature_names)
        return explainWithAnchorView(data, precision, coverage)
    elif method == "PFI":
        raw = explainWithPfi(model, X_test, y_test)
        return explainWithPfiView(raw, feature_names)
    else:
        return f"La méthode d'explicabilité {method} n'est pas encore disponible"

def explainWithLimeRaw(model, X_train, X_test, feature_names, class_names):
    explainer = LimeTabularExplainer( training_data=np.array(X_train), feature_names=feature_names, class_names=class_names, mode="classification")
    explanation = explainer.explain_instance(X_test[0], model.predict_proba)
    return explanation.as_list()

def explainWithShapRaw(model, X_train):
    explainer = shap.Explainer(model.predict, X_train)
    shap_values = explainer(X_train[:10])
    return shap_values

def explainWithAnchor(model, X_train, feature_names):
    explainer = AnchorTabular(predictor=model.predict, feature_names=feature_names)
    explainer.fit(X_train, disc_perc=(25, 50, 75))
    explanation = explainer.explain(X_train[0])
    return explanation.data['anchor'], explanation.data['precision'], explanation.data['coverage']

def explainWithPfi(model, X_test, y_test):
    results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
    return results

if __name__ == "__main__":
    print("hello world")

def explainWithLimeView(raw_result) -> str:
    html = "<ul class='list-group'>"
    for feature, weight in raw_result:
        color = 'text-success' if weight >= 0 else 'text-danger'
        html += f"<li class='list-group-item d-flex justify-content-between align-items-center'>"
        html += f"<span>{feature}</span>"
        html += f"<span class='{color}'><strong>{weight:.3f}</strong></span>"
        html += "</li>"
    html += "</ul>"
    return html

def explainWithShapView(shap_values, feature_names) -> str:
    plt.clf()
    shap.summary_plot(shap_values, features=shap_values.data, feature_names=feature_names, show=False)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    html = f"""
    <div class='text-center'>
        <img src='data:image/png;base64,{image_base64}' class='img-fluid' alt='SHAP Summary Plot'>
    </div>
    """
    return html

def explainWithAnchorView(anchor, precision, coverage) -> str:
    rule = "<p class='text-success'> ET </p>".join(anchor)
    html = f"""
    <div class='card'>
      <div class='card-body'>
        <p><strong>Règle d'ancrage :</strong> {rule}</p>
        <p><strong>Précision :</strong> {precision:.2f}</p>
        <p><strong>Couverture :</strong> {coverage:.2f}</p>
      </div>
    </div>
    """
    return html

def explainWithPfiView(result, feature_names) -> str:
    mean_importances = result.importances_mean
    std_importances = result.importances_std
    sorted_idx = np.argsort(-mean_importances)

    html = """
    <table class='table table-bordered table-striped'>
      <thead class='table-light'>
        <tr>
          <th>Feature</th>
          <th>Importance Moyenne</th>
          <th>Écart-type</th>
        </tr>
      </thead>
      <tbody>
    """
    for idx in sorted_idx[:10]:
        html += f"<tr><td>{feature_names[idx]}</td><td>{mean_importances[idx]:.4f}</td><td>{std_importances[idx]:.4f}</td></tr>"

    html += "</tbody></table>"
    return html

