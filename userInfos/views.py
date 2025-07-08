from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import PersonProfileForm
from .forms import TechnicalContextForm

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
            # on sauvegarde l'id dans la session pour le donner à la suite du formulaire
            request.session['profile_id'] = profile.id
            return redirect('models')
    else:
        form = PersonProfileForm()
    
    return render(request, 'userInfos/create_profile.html', {'form': form})

def create_technical_context(request):
    if request.method == 'POST':
        form = TechnicalContextForm(request.POST)
        if form.is_valid():
            context = form.save(commit=False)
            profile_id = request.session.get('profile_id')
            if profile_id:
                context.person_profile_id = profile_id
                context.save()
                request.session['technical_context_id'] = context.id
            return redirect('recommendation')
    else:
        form = TechnicalContextForm()

    return render(request, 'userInfos/technical_context.html', {'form': form})
