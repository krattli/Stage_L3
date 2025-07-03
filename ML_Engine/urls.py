from django.urls import path
from .views import model_view

urlpatterns = [
    path('models/', model_view, name='models'),
]
