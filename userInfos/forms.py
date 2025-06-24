from django import forms
from .models import PersonProfile
from .models import TechnicalContext

"""
Classe de formulaire qui serviera à renseigner le type utilisateur xAI
elle est assez simple, le reste est géré par django
"""
class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = PersonProfile
        exclude = ['owner', 'created_at']

class TechnicalContextForm(forms.ModelForm):
    class Meta:
        model = TechnicalContext
        fields = ['model_type', 'task_type', 'data_type']

