from lime.lime_tabular import LimeTabularExplainer
import alibi.api.interfaces as anchor
from alibi.explainers import AnchorTabular
from sklearn.inspection import permutation_importance
from sklearn.utils import Bunch
from typing import List, Union, Dict, Any
import shap
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

from ML_Engine.models import ModelType


class ExplainerResult:
    def __init__(self, html: str, json_data: Dict[str, Any]):
        self.html = html
        self.json_data = json_data

def getExplanationHtmlAndJson(X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str], method: str) -> ExplainerResult:
    explainer:BaseExplainer = AVAILABLE_EXPLAINERS[method]
    return explainer.explain(X_train, X_test, y_test, model, feature_names, class_names)

class BaseExplainer: # classe "abstraite"
    def explain(self, X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str]) -> ExplainerResult:
        raise NotImplementedError

class LimeExplainer(BaseExplainer):
    def explain(self, X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str]) -> ExplainerResult:
        raw_explanation = self._get_raw_explanation(model, X_train, X_test, feature_names, class_names)
        html = raw_explanation.as_html()
        json_data = self._to_json(raw_explanation)
        return ExplainerResult(html, json_data)
    
    def _get_raw_explanation(self, model, X_train, X_test, feature_names, class_names):
        explainer = LimeTabularExplainer( training_data=np.array(X_train), feature_names=feature_names, class_names=class_names, mode="classification")
        # On génère une explication locale pour une donnée locale, ici on a choisi la première de X_test mais on peux en prendre une autre
        # ce serait bien de : randomiser cette valeur de X qu'on veux expliquer la classification et de montrer ce x dans le résultat html
        explanation = explainer.explain_instance(X_test[0], model.predict_proba)
        return explanation
    
    def _to_json(self, explanation) -> Dict[str, Any]:
        feature_weights = explanation.as_list()
        intercept_value = None
        if hasattr(explanation, 'intercept'):
            if isinstance(explanation.intercept, dict):
                intercept_value = list(explanation.intercept.values())[0] if explanation.intercept else None
            else:
                intercept_value = explanation.intercept[0] if len(explanation.intercept) > 0 else None
        predict_proba = None
        if hasattr(explanation, 'predict_proba'):
            predict_proba = explanation.predict_proba.tolist()
        return {
            "method": "LIME",
            "feature_weights": [{"feature": feat, "weight": weight} for feat, weight in feature_weights],
            "score": getattr(explanation, 'score', None),
            "intercept": intercept_value,
            "predicted_class": getattr(explanation, 'predicted_value', None),
            "available_labels": getattr(explanation, 'available_labels', None),
            "class_names": getattr(explanation, 'class_names', None),
            "prediction_probabilities": predict_proba
        }

class ShapExplainer(BaseExplainer):
    def explain(self, X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str]) -> ExplainerResult:
        shap_values = self._get_raw_explanation(model, X_train)
        html = self._to_html(shap_values, feature_names)
        json_data = self._to_json(shap_values, feature_names)
        return ExplainerResult(html, json_data)
    
    def _get_raw_explanation(self, model, X_train):
        explainer: shap.Explainer = shap.Explainer(model.predict, X_train)
        shap_values = explainer(X_train[:10])  # dans le module shap, l'objet Explainer est callable, et son call return les shap-values
        return shap_values
    
    def _to_html(self, shap_values, feature_names) -> str:
        plt.clf()  # le plot est chargé en mémoire et pas rendu à l'écran directement
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
    
    def _to_json(self, shap_values, feature_names) -> Dict[str, Any]:
        return {
            "method": "SHAP",
            "shap_values": shap_values.values.tolist(),
            "base_values": shap_values.base_values.tolist(),
            "data": shap_values.data.tolist(),
            "feature_names": feature_names
        }

class AnchorExplainer(BaseExplainer):
    def explain(self, X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str]) -> ExplainerResult:
        anchor_data, precision, coverage = self._get_raw_explanation(model, X_train, feature_names)
        html = self._to_html(anchor_data, precision, coverage)
        json_data = self._to_json(anchor_data, precision, coverage)
        return ExplainerResult(html, json_data)
    
    def _get_raw_explanation(self, model, X_train, feature_names):
        # on a set le type de explainer juste pour que le lsp comprenne lorsqu'on veux aller à la déclaration des méthodes utilisées
        explainer: AnchorTabular = AnchorTabular(predictor=model.predict, feature_names=feature_names)
        explainer.fit(X_train, disc_perc=(25, 50, 75))
        explanation: anchor.Explanation = explainer.explain(X_train[0])  # pleins de paramètres à cette fonction
        return explanation.data['anchor'], explanation.data['precision'], explanation.data['coverage']  # Les trois champs du dict
    
    def _to_html(self, anchor_data, precision, coverage) -> str:
        rule = "<p class='text-success'> ET </p>".join(anchor_data)
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
    
    def _to_json(self, anchor_data, precision, coverage) -> Dict[str, Any]:
        return {
            "method": "ANCHOR",
            "anchor_rules": anchor_data,
            "precision": float(precision),
            "coverage": float(coverage)
        }

class PfiExplainer(BaseExplainer):
    def explain(self, X_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, model: ModelType, feature_names: List[str], class_names: List[str]) -> ExplainerResult:
        result = self._get_raw_explanation(model, X_test, y_test)
        html = self._to_html(result, feature_names)
        json_data = self._to_json(result, feature_names)
        return ExplainerResult(html, json_data)
    
    def _get_raw_explanation(self, model, X_test, y_test) -> Union[Bunch, dict]:
        # va nous donner un Bunch ou un Dict de Bunch qui va classer les paramètres de départ selon leurs importance en en faisant des permutations
        results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
        return results
    
    def _to_html(self, result, feature_names) -> str:
        mean_importances = result.importances_mean
        std_importances = result.importances_std
        sorted_importances = np.argsort(-mean_importances)  # on sort bien l'array pour qu'il donne les importances dans un ordre décroissant

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
    
    def _to_json(self, result, feature_names) -> Dict[str, Any]:
        mean_importances = result.importances_mean
        std_importances = result.importances_std
        sorted_indices = np.argsort(-mean_importances)
        return {
            "method": "PFI",
            "feature_importances": [
                {
                    "feature": feature_names[i],
                    "importance_mean": float(mean_importances[i]),
                    "importance_std": float(std_importances[i]),
                    "rank": rank + 1
                }
                for rank, i in enumerate(sorted_indices)
            ]
        }

if __name__ == "__main__":
    print("hello world")

AVAILABLE_EXPLAINERS = {
    "LIME": LimeExplainer(),
    "SHAP": ShapExplainer(),
    "ANCHOR": AnchorExplainer(),
    "PFI": PfiExplainer()
}

# on conserve quand même l'ancienne version du code
def explainWithLimeRaw(model, X_train, X_test, feature_names, class_names):
    explainer = LimeTabularExplainer(training_data=np.array(X_train), feature_names=feature_names, class_names=class_names, mode="classification")
    explanation = explainer.explain_instance(X_test[0], model.predict_proba)
    return explanation.as_html()

def explainWithShapRaw(model, X_train):
    explainer: shap.Explainer = shap.Explainer(model.predict, X_train)
    shap_values = explainer(X_train[:10])
    return shap_values

def explainWithAnchor(model, X_train, feature_names):
    explainer: AnchorTabular = AnchorTabular(predictor=model.predict, feature_names=feature_names)
    explainer.fit(X_train, disc_perc=(25, 50, 75))
    explanation: anchor.Explanation = explainer.explain(X_train[0])
    return explanation.data['anchor'], explanation.data['precision'], explanation.data['coverage']

def explainWithPfi(model, X_test, y_test) -> Union[Bunch, dict]:
    results = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0)
    return results

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
    plt.clf()
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
    sorted_importances = np.argsort(-mean_importances)

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
