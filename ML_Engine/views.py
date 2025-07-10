from django.shortcuts import render, redirect
from .forms import ModelChoiceForm
from .xAI_ModelTraining import getModelPredictions, getReportFromData
from .forms import ModelChoiceForm, ExplainabilityChoiceForm
from .xAI_explainer import getExplanationHTML

def xAIrecommendationController(request):
    if request.POST.get("goToEval"):
        return redirect("eval")
    model_name = request.session.get('recommended_model')
    xai_method = request.session.get('recommended_xai')
    X_train, X_test, y_train, y_test, y_pred, trained_model, feature_names = getModelPredictions(model_name)
    confusionMatrixImg, usefullStats = getReportFromData(y_test, y_pred, model_name)
    explanation_html = getExplanationHTML(X_train, X_test, y_test, trained_model, feature_names, xai_method)
    return render(request, 'explainerRecommendation.html', {
        'image_base64': confusionMatrixImg,
        'report': usefullStats,
        'explanation': explanation_html
    })

def modelDebugController(request):
    confusionMatrixImg = None
    usefullStats = None
    explanation_html = None

    if request.method == 'POST':
        modelChoiceForm = ModelChoiceForm(request.POST)
        explainabilityChoiceForm = ExplainabilityChoiceForm(request.POST)

        if modelChoiceForm.is_valid():
            # if explainabilityChoiceForm.is_valid() and request.POST.get("goToEval"):
            #     return redirect("eval")
            model_name = modelChoiceForm.cleaned_data['modelName']
            X_train, X_test, y_train, y_test, y_pred, trained_model, feature_names = getModelPredictions(model_name)
            confusionMatrixImg, usefullStats = getReportFromData(y_test, y_pred, model_name)

            if explainabilityChoiceForm.is_valid():
                method = explainabilityChoiceForm.cleaned_data['explainer']
                explanation_html = getExplanationHTML(X_train, X_test, y_test, trained_model, feature_names, method)
    else:
        modelChoiceForm = ModelChoiceForm()
        explainabilityChoiceForm = ExplainabilityChoiceForm()

    return render(request, 'debugModel.html', {
        'form': modelChoiceForm,
        'explain_form': explainabilityChoiceForm,
        'image_base64': confusionMatrixImg,
        'report': usefullStats,
        'explanation': explanation_html
    })
