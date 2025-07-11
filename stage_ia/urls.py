"""
URL configuration for stage_ia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from stage_ia import views as global_views

urlpatterns = [
    path('', global_views.home, name='homepage'),
    path("user/", include('userInfos.urls')),
    path("user/", include('xAI_eval.urls')),
    path("user/", include('ML_Engine.urls')),
    path('admin/', admin.site.urls),
]
