from django.urls import path
from .views import evaluationView

urlpatterns = [
    path('eval/', evaluationView, name='eval'),
]
