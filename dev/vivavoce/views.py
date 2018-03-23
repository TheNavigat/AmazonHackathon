from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from .forms import UploadFileForm

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

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # TODO: Add else clause and add handling
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponse(status=200)
    return HttpResponse(status=400)


class RecordView(generic.TemplateView):
    template_name = 'vivavoce/record.html'
# Create your views here.
