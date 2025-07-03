from django.shortcuts import render
from .forms import ModelChoiceForm
from .aiModel import getReport

def model_view(request):
    confusionMatrixImg = None
    usefullStats = None
    if request.method == 'POST':
        form = ModelChoiceForm(request.POST)
        if form.is_valid():
            model = form.cleaned_data['modelName']
            confusionMatrixImg, usefullStats = getReport(model)
    else:
        form = ModelChoiceForm()
    return render(request, 'ML_Engine/debugModel.html', {
        'form': form,
        'image_base64': confusionMatrixImg,
        'report': usefullStats
    })
