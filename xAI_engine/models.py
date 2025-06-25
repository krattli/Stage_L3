from django.db import models

class Recommendation(models.Model):

    class TaskType:
        CLASSIFICATION = "classification"
        REGRESSION = "regression"

    TASK_CHOICES = [
        (TaskType.CLASSIFICATION, 'Classification'),
        (TaskType.REGRESSION, 'Régression'),
    ]

    class Explainer:
        LIME = "LIME"
        SHAP = "SHAP"
        PFI = "PFI"
        ANCHOR = "ANCHOR"
        INTEGRATED_GRADIENTS = "INTEGRATED_GRADIENTS"
        GRAD_CAM = "GRAD_CAM"
        COUNTERFACTUAL = "COUNTERFACTUAL"
        SURROGATE = "SURROGATE"
        DEEP_LIFT = "DEEP_LIFT"

    EXPLAINER_CHOICES = [
        (Explainer.LIME, 'LIME'),
        (Explainer.SHAP, 'SHAP'),
        (Explainer.PFI, 'Permutation Feature Importance (PFI)'),
        (Explainer.ANCHOR, 'Anchor'),
        (Explainer.INTEGRATED_GRADIENTS, 'Integrated Gradients'),
        (Explainer.GRAD_CAM, 'Grad-CAM'),
        (Explainer.COUNTERFACTUAL, 'CounterFactual Explainations'),
        (Explainer.SURROGATE, 'Surrogate Models'),
        (Explainer.DEEP_LIFT, 'DeepLIFT'),
    ]

    task_type = models.CharField(max_length=20, choices=TASK_CHOICES)
    explainer = models.CharField(max_length=30, choices=EXPLAINER_CHOICES)

    def __str__(self):
        return f"{self.explainer}"
