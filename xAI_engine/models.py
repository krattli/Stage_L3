from django.db import models
from enum import Enum

class Recommendation(models.Model):

    class Explainer(Enum):
        LIME = "LIME"
        SHAP = "SHAP"
        PFI = "PFI"
        ANCHOR = "ANCHOR"
        # on verra si on fais les suivants
        # GRAD_CAM = "GRAD_CAM" # innutile dans ce contexte
        # COUNTERFACTUAL = "COUNTERFACTUAL"
        # SURROGATE = "SURROGATE"

    EXPLAINER_CHOICES = [
        (Explainer.LIME, 'LIME'),
        (Explainer.SHAP, 'SHAP'),
        (Explainer.PFI, 'Permutation Feature Importance (PFI)'),
        (Explainer.ANCHOR, 'Anchor'),
        # (Explainer.GRAD_CAM, 'Grad-CAM'),
        # (Explainer.COUNTERFACTUAL, 'CounterFactual Explainations'),
        # (Explainer.SURROGATE, 'Surrogate Models'),
    ]

    explainer = models.CharField(max_length=30, choices=EXPLAINER_CHOICES)

    def __str__(self):
        return f"{self.explainer}"
