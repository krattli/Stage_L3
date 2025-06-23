from django import forms
from .models import PersonProfile

"""
Classe de formulaire qui serviera à renseigner le type utilisateur xAI
elle est assez simple, le reste est géré par django
"""
class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = PersonProfile
        exclude = ['owner', 'created_at']
