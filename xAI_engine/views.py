from django.shortcuts import render
#from .models import Recommendation
from userInfos.models import PersonProfile, TechnicalContext
from .engine import recommendation_engine

def recommend_method(request):
    profile_id = request.session.get('profile_id')
    technical_context_id = request.session.get('technical_context_id')

    profile = PersonProfile.objects.get(id=profile_id)
    context = TechnicalContext.objects.get(id=technical_context_id)

    recommandation = recommendation_engine(profile, context)

    return render(request, 'xAI_engine/result.html', {'profile': profile, 'context': context, 'recommandation':recommandation})
