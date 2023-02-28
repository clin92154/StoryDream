from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def savebook(request):
    settings={
        'bookID':123
    }
    return render(request,'savebook/save.html',settings)