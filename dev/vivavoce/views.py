from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import json


def index(request):
    User = {}
    User['fullname']= 'Karim ElGhandour'
    Exam = {}
    Exam['name'] = 'Psychology'
    return render(request, 'vivavoce/index.html', {'User': User,'Exam':Exam,})

def start(request):
    Question = {}
    Question['number']= '2'
    Question['total']= '30'

    return render(request, 'vivavoce/start.html', {'Question': Question})

# Create your views here.
