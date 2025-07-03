from django import forms
from .models import AvailableModels

class ModelChoiceForm(forms.Form):
    MODEL_CHOICES = [(m.name, m.name.replace("_", " ")) for m in list(AvailableModels.BlackboxModels) + list(AvailableModels.WhiteBoxModels)]
    modelName = forms.ChoiceField(choices=MODEL_CHOICES, label="choisissez parmis les modèles disponiobles")
