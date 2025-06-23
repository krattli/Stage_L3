from django.db import models
from django.contrib.auth.models import User

"""
Classe PersonProfile de notre app django
elle contiendra touts les champs demandés pour faire notre app et elle est à décoreller de la classe utilisateur global
Un utilisateur global pourra tester les recommandations de techniques d'explicabilité sur plusieurs types de profiles comme celui ci
"""
class PersonProfile(models.Model):
    # champs du profil user possibles utilisés dans l'algo de reco x AI
    ROLE_CHOICES = [
        ('student', 'Étudiant'),
        ('researcher', 'Chercheur'),
        ('data_scientist', 'Data Scientist'),
    ]
    EXPERTISE_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('expert', 'Expert'),
    ]
    DOMAIN_CHOICES = [
        ('health', 'Santé'),
        ('finance', 'Finance'),
        ('education', 'Éducation'),
    ]
    VISUAL_PREF_CHOICES = [
        ('graph', 'Graphes'),
        ('table', 'Tableaux'),
        ('text', 'Texte explicatif'),
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
