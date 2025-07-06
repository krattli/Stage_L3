from django.shortcuts import render
from .forms import ModelChoiceForm
from .xAI_ModelTraining import getReport
from .forms import ModelChoiceForm, ExplainabilityChoiceForm
from .xAI_ModelTraining import getReport
from .xAI_explainer import getExplanation

def model_view(request):
    confusionMatrixImg = None
    usefullStats = None
    explanation_result = None
    model = None

    if request.method == 'POST':
        form = ModelChoiceForm(request.POST)
        explain_form = ExplainabilityChoiceForm(request.POST)

        if form.is_valid():
            model = form.cleaned_data['modelName']
            confusionMatrixImg, usefullStats = getReport(model)

            if explain_form.is_valid():
                method = explain_form.cleaned_data['explainer']
                try:
                    explanation_result = getExplanation(model, method)
                except Exception as e:
                    explanation_result = f"Erreur pendant l'explication : {str(e)}"
    else:
        form = ModelChoiceForm()
        explain_form = ExplainabilityChoiceForm()

    return render(request, 'ML_Engine/debugModel.html', {
        'form': form,
        'explain_form': explain_form,
        'image_base64': confusionMatrixImg,
        'report': usefullStats,
        'explanation': explanation_result
    })

