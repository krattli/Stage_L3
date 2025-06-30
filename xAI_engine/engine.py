from .models import Recommendation
from userInfos.models import PersonProfile, TechnicalContext

def recommendation_engine(p:PersonProfile, t:TechnicalContext) -> Recommendation:
    # On fait un double appel à cette fonction car à l'avenir on pourra écrire d'autres fonctions de recommendation
    return recommendation_engine_rule_based(p,t)

def recommendation_engine_rule_based(p: PersonProfile, t: TechnicalContext) -> Recommendation:
    """
    Recommande une ia explicative en se basant sur des règles fixes
    liées au profil utilisateur et au contexte technique.
    Le résultat est un objet Recommendation correspondant à la méthode d'explicabilité choisie.
    """
    explainer_choice = None

    # On commence par des règles spécifiques basées sur les préférences visuelles de l'utilisateur
        # Si l'utilisateur préfère des explications plus visuelles et graphiques et que les données sont des images,
        # Grad-CAM donne une explication plutôt graphique avec ses heatmaps
    if p.visual_pref == PersonProfile.VisualPref.GRAPH and t.data_type == TechnicalContext.DataType.IMG:
        explainer_choice = Recommendation.Explainer.GRAD_CAM
        # Si l'utilisateur préfère une explication avec du texte et que l'IA fais de la classification,
        # Les règles textuelles d'ANCHOR sont surement très compréhensibles
        # règles doivent être similaires
    elif p.visual_pref == PersonProfile.VisualPref.TEXTE and t.task_type == TechnicalContext.TaskType.CLASSIFICATION:
        explainer_choice = Recommendation.Explainer.ANCHOR
        # Si l'utilisateur préfère un format de tableau
        # on peut utiliser la permutation qui donnera un classement de tout les paramètres du modèle selon leur importance dans un tableau
    elif p.visual_pref == PersonProfile.VisualPref.TABLE:
        explainer_choice = Recommendation.Explainer.PFI

    # Ensuite, il est assez pertinent de prendre ensuite en critère le niveau d'expertise en IA déclaré du sondé
    if explainer_choice is None: # bien sur, on fais un choix uniquement si le modèle n'a pas été choisi précédemment
        if p.expertise == PersonProfile.Expertise.DEBUTANT:
            # Utilisateur débutant : on privilégie des méthodes locales plus simples et intuitives, elles ont plus de risques d'être comprises facilement
            if t.task_type == TechnicalContext.TaskType.CLASSIFICATION and (t.data_type == TechnicalContext.DataType.TAB or t.data_type == TechnicalContext.DataType.TXT):
                explainer_choice = Recommendation.Explainer.ANCHOR    #
            elif t.data_type == TechnicalContext.DataType.IMG:
                explainer_choice = Recommendation.Explainer.GRAD_CAM  # pour des images, Grad-CAM est juste très bien, il est simple, intuitif et très complet avec ses heatmaps
            elif t.task_type == TechnicalContext.TaskType.REGRESSION:
                explainer_choice = Recommendation.Explainer.PFI       # Pour de la régression, on peut donner une explication avec la permutation  des features
            else:
                explainer_choice = Recommendation.Explainer.ANCHOR    # Choix par défaut pour un débutant (ce modèle a des bons scores de compréhension dans le mémoire)
        elif p.expertise == PersonProfile.Expertise.INTERMEDIAIRE:
            # Utilisateur intermédiaire : on peut introduire des méthodes un peu plus avancées (comme SHAP ou LIME par exemple)
            if t.data_type == TechnicalContext.DataType.IMG:
                explainer_choice = Recommendation.Explainer.GRAD_CAM  # Pas de raison de changer ici
            elif t.data_type == TechnicalContext.DataType.TXT:
                if t.model_type == TechnicalContext.ModelType.DEEP_LEARNING:
                    explainer_choice = Recommendation.Explainer.SHAP  # Pour un modèle de réseau de neurone plus complexe, SHAP peux fournir des bonnes contributions locales des mots
                else:
                    explainer_choice = Recommendation.Explainer.LIME  # Pour un modèle texte plus simple LIME est suffiant je pense
            elif t.data_type == TechnicalContext.DataType.TAB:
                if t.task_type == TechnicalContext.TaskType.CLASSIFICATION:
                    explainer_choice = Recommendation.Explainer.SHAP  # SHAP donne des explications locales/globales détaillées pour les modèles tabulaires
                else:
                    explainer_choice = Recommendation.Explainer.SHAP  # Pour régression tabulaire également, SHAP est approprié (ex. valeurs de Shapley globales)
            else:
                explainer_choice = Recommendation.Explainer.SHAP      # Par défaut pour intermédiaire, SHAP est un bon compromis (puissant mais plus exigeant)
        elif p.expertise == PersonProfile.Expertise.EXPERT:
            # Utilisateur expert : on privilégie les méthodes les plus avancées, plus dures à comprendre et plus demandeuses car pouvant fournir des explications très précises
            if t.data_type == TechnicalContext.DataType.IMG: # ici comme l'utilisateur est plus avancé, on va donner d'autres modèles que Grad-CAM (même si je suis pas sur que ce soit une bonne idée)
                if t.model_type == TechnicalContext.ModelType.DEEP_LEARNING:
                    explainer_choice = Recommendation.Explainer.INTEGRATED_GRADIENTS  # Pour réseaux de neurones sur images, la méthode des gradients donne des explications fines
                else:
                    explainer_choice = Recommendation.Explainer.GRAD_CAM  # sinon, pour les autres modèles, on peux revenir sur du Grad-CAM
            elif t.data_type == TechnicalContext.DataType.TXT:
                explainer_choice = Recommendation.Explainer.SHAP      # Un profile expert saura surement interpréter les valeurs de Shapley sur des données de type texte
            elif t.data_type == TechnicalContext.DataType.TAB:
                explainer_choice = Recommendation.Explainer.SHAP      # Pour données tabulaires un expert appréciera la polyvalence de SHAP (avec les features d'importance locales et globales)
            else:
                explainer_choice = Recommendation.Explainer.INTEGRATED_GRADIENTS      # Par défaut pour un expert

    # au cas ou aucune règle n'a permis d'assigner un modèle d'explicabilité, on en met un par défault (pas sur que cette condition soit atteinte mais bon)
    # on prend ANCHOR par défaut car c'est une méthode globalement applicable et compréhensible par tous
    if explainer_choice is None:
        explainer_choice = Recommendation.Explainer.ANCHOR

    # Retourne l'objet Recommendation correspondant à la méthode choisie.
    return Recommendation(explainer=explainer_choice)

# pas terminée
def recommendation_engine_weighted(p: PersonProfile, t: TechnicalContext) -> Recommendation:
    """
    Recommande une méthode d'explicabilité en attribuant et modifiant un score
    à chaque candidat en fonction du profil utilisateur et du contexte technique.
    à la fin, la méthode avec le score le plus élevé est sélectionnée.
    Retourne l'objet Recommendation correspondant à cette méthode.
    """

    scores = {explainer: 0 for explainer, _ in Recommendation.EXPLAINER_CHOICES}

    # Pondération par niveau d'expertise de l'utilisateur
    if p.expertise == PersonProfile.Expertise.DEBUTANT:
        # Débutant : on va favoriser les méthodes les plus simples à comprendre
        scores[Recommendation.Explainer.ANCHOR] += 2
        scores[Recommendation.Explainer.PFI] += 1

    # Pondération par type de données
    if t.data_type == TechnicalContext.DataType.IMG:
        scores[Recommendation.Explainer.GRAD_CAM] += 3   # Grad-CAM est très adapté aux données type images avec les heatmaps qu'elle donne
        scores[Recommendation.Explainer.INTEGRATED_GRADIENTS] += 2  # Integrated Gradients utile pour images lorsqu'il y a des réseaux de neurones impliqués
    return Recommendation.objects.create(explainer=None)
