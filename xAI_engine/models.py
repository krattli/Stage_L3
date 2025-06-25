from django.db import models
class Recommendation(models.Model):

    TASK_CHOICES = [
        ('classification', 'Classification'),
        ('regression', 'Régression'),
    ]

    EXPLAINER_CHOICES = [
        ('lime', 'LIME'),
        ('shap', 'SHAP'),
        ('PFI', 'Permutation Feature Importance (PFI)'),
        ('anchor', 'Anchor'),
        ('IG', 'Integrated Gradients'),
        ('GC', 'Grad-CAM'),
        ('CE', 'CounterFactual Explainations'),
        ('SM', 'Surrogate Models'),
        ('DL', 'DeepLIFT'),
    ]

    task_type = models.CharField(max_length=20, choices=TASK_CHOICES)
    explainer = models.CharField(max_length=20, choices=EXPLAINER_CHOICES)

    def __str__(self):
        return f"{self.explainer}"

