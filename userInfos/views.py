from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import PersonProfileForm

# créé le formulaire pour créer un template utilisateur xAI
def create_person_profile(request):
    if request.method == 'POST':
        form = PersonProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            if request.user.is_authenticated:
                profile.owner = request.user
            else:
                profile.owner = None
            profile.save()
            return redirect('/')
    else:
        form = PersonProfileForm()
    
    return render(request, 'userInfos/create_profile.html', {'form': form})

# controlleur
def home(request):
    return render(request, 'home.html')

