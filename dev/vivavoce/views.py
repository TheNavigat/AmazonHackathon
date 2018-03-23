from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .forms import UploadFileForm
from .libraries import s3
from .models import Question

def index(request):
    User = {}
    User['fullname']= 'Karim ElGhandour'
    Exam = {}
    Exam['name'] = 'Psychology'
    return render(request, 'vivavoce/index.html', {'User': User,'Exam':Exam,})

def start(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'vivavoce/start.html', { 'question': question, 'count': Question.objects.count() })

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # TODO: Add else clause and add handling
        if form.is_valid():
            print(request.FILES)
            # handle_uploaded_file(request.FILES['file'])
            s3.upload_to_s3(request.FILES['file'].read())
            return HttpResponse(status=200)
    return HttpResponse(status=400)


class RecordView(generic.TemplateView):
    template_name = 'vivavoce/record.html'
# Create your views here.
