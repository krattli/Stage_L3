from django.shortcuts import render

def evaluationView(request):
    return render(request, 'eval.html')
