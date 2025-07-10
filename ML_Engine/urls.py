from django.urls import path
from .views import modelDebugController, xAIrecommendationController

urlpatterns = [
    path('models_debug/', modelDebugController, name='model_debug'),
    path('xAI_recommendation', xAIrecommendationController, name='xAI_recommendation'),
]
