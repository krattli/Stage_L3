from .models import Recommendation
from userInfos.models import PersonProfile, TechnicalContext

def recommendation_engine(p:PersonProfile, t:TechnicalContext) -> Recommendation:
    recommendation = Recommendation()
    recommendation.explainer = 'LIME'
    return recommendation
