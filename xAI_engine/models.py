from django.db import models

class Recommendation(models.Model):

    class Explainer:
        # techniques d'explicabilités utilisés dans le mémoire
        LIME = "LIME"
        SHAP = "SHAP"
        PFI = "PFI"
        ANCHOR = "ANCHOR"
        # à supprimer
        LOGISTIC_REGRESSION = "LOGISTIC_REGRESSION" # white box
        DECISION_TREE = "DECISION_TREE"
        NAIVE_BAYES = "NAIVE_BAYES"
        # autres modèles mentionnés dans le mémoire
        INTEGRATED_GRADIENTS = "INTEGRATED_GRADIENTS" #supprimer
        GRAD_CAM = "GRAD_CAM"
        COUNTERFACTUAL = "COUNTERFACTUAL"
        SURROGATE = "SURROGATE"
        DEEP_LIFT = "DEEP_LIFT" # supprimer

    EXPLAINER_CHOICES = [
        (Explainer.LIME, 'LIME'),
        (Explainer.SHAP, 'SHAP'),
        (Explainer.PFI, 'Permutation Feature Importance (PFI)'),
        (Explainer.ANCHOR, 'Anchor'),
        (Explainer.LOGISTIC_REGRESSION, "Logistic regression"),
        (Explainer.DECISION_TREE, "Decision tree"),
        (Explainer.NAIVE_BAYES, "Naive bayes"),
        (Explainer.INTEGRATED_GRADIENTS, 'Integrated Gradients'),
        (Explainer.GRAD_CAM, 'Grad-CAM'),
        (Explainer.COUNTERFACTUAL, 'CounterFactual Explainations'),
        (Explainer.SURROGATE, 'Surrogate Models'),
        (Explainer.DEEP_LIFT, 'DeepLIFT'),
    ]

    explainer = models.CharField(max_length=30, choices=EXPLAINER_CHOICES)

    def __str__(self):
        return f"{self.explainer}"
