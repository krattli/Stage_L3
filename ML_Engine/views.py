from django.shortcuts import render
from .forms import ModelChoiceForm
from .xAI_ModelTraining import getModelPredictions, getReportFromData
from .forms import ModelChoiceForm, ExplainabilityChoiceForm
from .xAI_explainer import getExplanation

def model_view(request):
    confusionMatrixImg = None
    usefullStats = None
    explanation_result = None

    if request.method == 'POST':
        modelChoiceForm = ModelChoiceForm(request.POST)
        explainabilityChoiceForm = ExplainabilityChoiceForm(request.POST)

        if modelChoiceForm.is_valid():
            model = modelChoiceForm.cleaned_data['modelName']
            X_train, X_test, y_train, y_test, y_pred, trained_model, feature_names = getModelPredictions(model)
            confusionMatrixImg, usefullStats = getReportFromData(y_test, y_pred)

            if explainabilityChoiceForm.is_valid():
                method = explainabilityChoiceForm.cleaned_data['explainer']
                try:
                    explanation_result = getExplanation(X_train, X_test, y_test, trained_model, feature_names, method)
                except Exception as e:
                    explanation_result = f"Erreur pendant l'explication : {str(e)}"
    else:
        modelChoiceForm = ModelChoiceForm()
        explainabilityChoiceForm = ExplainabilityChoiceForm()

    return render(request, 'ML_Engine/debugModel.html', {
        'form': modelChoiceForm,
        'explain_form': explainabilityChoiceForm,
        'image_base64': confusionMatrixImg,
        'report': usefullStats,
        'explanation': explanation_result
    })
