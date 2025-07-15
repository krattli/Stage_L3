from lime.lime_tabular import LimeTabularExplainer
import alibi.api.interfaces as anchor
from alibi.explainers import AnchorTabular
from sklearn.inspection import permutation_importance
from sklearn.utils import Bunch
from typing import List, Union
import shap
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

from ML_Engine.models import ModelType

def getExplanationHTML(X_train:np.ndarray, X_test:np.ndarray, y_test:np.ndarray, model:ModelType, feature_names:List[str], class_names:List[str], method:str) -> str:
    if method == "LIME":
        raw =  explainWithLimeRaw(model, X_train, X_test, feature_names, class_names)
        # return explainWithLimeView(raw)
        return raw
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
        return f"La méthode d'explicabilité {method} n'est pas encore disponible" # ne sera jamais atteint mais si je ne la met pas, pyright s'énerve

def explainWithLimeRaw(model, X_train, X_test, feature_names, class_names):
    explainer = LimeTabularExplainer( training_data=np.array(X_train), feature_names=feature_names, class_names=class_names, mode="classification")
    # On génère une explication locale pour une donnée locale, ici on a choisi la première de X_test mais on peux en prendre une autre
    # ce serait bien de : randomiser cette valeur de X qu'on veux expliquer la classification et de montrer ce x dans le résultat html
    explanation = explainer.explain_instance(X_test[0], model.predict_proba) # return un objet Explaination
    return explanation.as_html() # possibilité de faire une explication sous une autre forme : la fonction as_pyplot_figure

def explainWithShapRaw(model, X_train):
    explainer:shap.Explainer = shap.Explainer(model.predict, X_train)
    shap_values = explainer(X_train[:10]) # dans le module shap, l'objet Explainer est callable, et son call return les shap-values
    return shap_values

def explainWithAnchor(model, X_train, feature_names):
    # on a set le type de explainer juste pour que le lsp comprenne lorsqu'on veux aller à la déclaration des méthodes utilisées
    explainer:AnchorTabular = AnchorTabular(predictor=model.predict, feature_names=feature_names)
    explainer.fit(X_train, disc_perc=(25, 50, 75))
    explanation:anchor.Explanation = explainer.explain(X_train[0]) # pleins de paramètres à cette fonction
    return explanation.data['anchor'], explanation.data['precision'], explanation.data['coverage'] # Les trois champs du dict

def explainWithPfi(model, X_test, y_test) -> Union[Bunch, dict]:
    # va nous donner un Bunch ou un Dict de Bunch qui va classer les paramètres de départ selon leurs importance en en faisant des permutations
    results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
    return results


if __name__ == "__main__":
    print("hello world")

# une méthode par défault du package lime fais également très bien le travail pour présenter les résultats en html, c'est juste plus moche
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
    plt.clf() # le plot est chargé en mémoire et pas rendu à l'écran directement
    # on utilise une méthode par défault du module shap pour qu'il fasse un plot graphique imagé des valeurs de shapley
    shap.summary_plot(shap_values, features=shap_values.data, feature_names=feature_names, show=False)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
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
    sorted_importances = np.argsort(-mean_importances) # on sort bien l'array pour qu'il donne les importances dans un ordre décroissant

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
    for i in sorted_importances[:10]:
        html += f"<tr><td>{feature_names[i]}</td><td>{mean_importances[i]:.4f}</td><td>{std_importances[i]:.4f}</td></tr>"

    html += "</tbody></table>"
    return html

