from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-profile/', views.create_person_profile, name='create_person_profile'),
]

