from django import forms
from .models import AvailableModels
from xAI_engine.models import Recommendation

class ModelChoiceForm(forms.Form):
    MODEL_CHOICES = [(m.name, m.name.replace("_", " ")) for m in list(AvailableModels.BlackboxModels) + list(AvailableModels.WhiteBoxModels)]
    modelName = forms.ChoiceField(choices=MODEL_CHOICES, label="choisissez parmis les modèles disponiobles")

class ExplainabilityChoiceForm(forms.Form):
    EXPLAINER_CHOICES = [(m.name, m.name.replace("_", " ")) for m in list(Recommendation.Explainer)]
    explainer = forms.ChoiceField(choices=EXPLAINER_CHOICES, label="Choisissez une méthode d'explicabilité")
