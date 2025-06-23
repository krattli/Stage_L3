from django.shortcuts import render
from userInfos.models import PersonProfile

def home(request):
    if not request.user.is_authenticated:
        profiles_without_owner = PersonProfile.objects.filter(owner__isnull=True)
    else:
        profiles_without_owner = None
    return render(request, 'home.html', {'profiles_without_owner': profiles_without_owner})
