from django.urls import path
from . import views

urlpatterns = [
    path('create-profile/', views.create_person_profile, name='create_person_profile'),
    #path('technical_context/', views.create_technical_context, name='technical_context'), # inutilisé
]

