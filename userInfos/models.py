from enum import Enum
from django.db import models
from django.contrib.auth.models import User

class PersonProfile(models.Model):
    """
    Classe PersonProfile de notre app django
    elle contiendra touts les champs demandés pour faire notre app et elle est à décoreller de la classe utilisateur global
    Un utilisateur global pourra tester les recommandations de techniques d'explicabilité sur plusieurs types de profiles comme celui ci
    """
    # Pour chaque attribut auquel l'utilisateur aura des choix, django met à disposition les attributs choices
    # C'est comme une sorte d'enum, elle prends la forme d'une liste de tuple de 2 elements
    # Ici on a ajouté une classe dans le tuple pour plus de réutilisabilité 
    # C'est un peu verbeux mais c'est la solution la plus efficace pour que le code soit consistant
    class Role():
        STUDENT = "étudiant"
        CHERCHEUR = "chercheur"
        PROF = "professeur"
        DATA_SCIENTIST = "Data Scientist"

    ROLE_CHOICES = [
        (Role.STUDENT, 'Étudiant'),
        (Role.CHERCHEUR, 'Chercheur'),
        (Role.PROF, 'Professeur'),
        (Role.DATA_SCIENTIST, 'Data Scientist'),
    ]

    class Expertise():
        DEBUTANT = "Débutant"
        INTERMEDIAIRE = "intermédiaire"
        AVANCED = "avancé"
        EXPERT = "expert"

    EXPERTISE_CHOICES = [
        (Expertise.DEBUTANT, 'Débutant'),
        (Expertise.INTERMEDIAIRE, 'Intermédiaire'),
        (Expertise.EXPERT, 'Expert'),
    ]

    class Domain:
        HEALTH = "health"
        MATH = "math"
        INFO = "info"
        FINANCE = "finance"
        EDUCATION = "education"
        SECONDAIRE = "secondaire"

    DOMAIN_CHOICES = [
        (Domain.HEALTH, "Santé"),
        (Domain.MATH, "Mathématiques"),
        (Domain.INFO, "Informatique"),
        (Domain.FINANCE, "Finance"),
        (Domain.EDUCATION, "Éducation"),
        (Domain.SECONDAIRE, "Éducation secondaire"),
    ]

    class VisualPref:
        GRAPH = "graph"
        TABLE = "table"
        TEXTE = "texte"

    VISUAL_PREF_CHOICES = [
        (VisualPref.GRAPH, "Graphes"),
        (VisualPref.TABLE, "Tableaux"),
        (VisualPref.TEXTE, "Texte explicatif"),
    ]

    # relation oneToMany à un utilisateur global de notre app django
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person_profile", null=True, blank=True)

    # Champs de l'entité PersonProfile
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    expertise = models.CharField(max_length=20, choices=EXPERTISE_CHOICES)
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    visual_pref = models.CharField(max_length=20, choices=VISUAL_PREF_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.domain}"

# Attention, il existe une autre classe qui définit les modèles disponibles
class ModelType(Enum):
    LOGISTIC_REGRESSION = "LOGISTIC_REGRESSION"
    DECISION_TREE = "DECISION_TREE"
    K_NEAREST_NEIGHBOUR = "KNN"
    NAIVE_BAYES = "NAIVE_BAYES"
    RANDOM_FOREST = "RANDOM_FOREST"
    EXTRA_TREES = "EXTRA_TREES"
    BAGGING = "BAGGING"
    GRADIENT_BOOSTING = "GRADIENT_BOOSTING"
    MLP = "MLP"
    DL = "MLP"

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

# à supprimer
"""
class TechnicalContext(models.Model):

    MODEL_CHOICES = [
        (ModelType.SVM, "SVM"),
        (ModelType.LOGISTIC_REGRESSION, "Logistic Regression"),
        (ModelType.DECISION_TREE, "Decision Tree"),
        (ModelType.K_NEAREST_NEIGHBOUR, "K-Nearest Neighbour"),
        (ModelType.NAIVE_BAYES, "Naive Bayes"),
        (ModelType.RANDOM_FOREST, "Random Forest"),
        (ModelType.EXTRA_TREES, "Extra Trees"),
        (ModelType.BAG, "Bagging"),
        (ModelType.GRADIENT_BOOSTING, "Gradient Boosting"),
        (ModelType.MLP, "MLP"),
        (ModelType.DEEP_LEARNING, "Deep Learning"),
    ]

    class TaskType:
        CLASSIFICATION = "C"
        REGRESSION = "R"

    TASK_CHOICES = [
        (TaskType.CLASSIFICATION, "Classification"),
        (TaskType.REGRESSION, "Régression"),
    ]

    class DataType:
        IMG = "img"
        TXT = "txt"
        TAB = "tab"

    DATA_TYPE_CHOICES = [
        (DataType.IMG, "Images"),
        (DataType.TXT, "Texte"),
        (DataType.TAB, "Tabulaires"),
    ]

    person_profile = models.OneToOneField( PersonProfile, on_delete=models.CASCADE, related_name='technical_context')
    model_type = models.CharField(max_length=50, choices=MODEL_CHOICES)
    task_type = models.CharField(max_length=50, choices=TASK_CHOICES)
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)

    def __str__(self):
        return f"Contexte technique pour {self.person_profile}"
"""
