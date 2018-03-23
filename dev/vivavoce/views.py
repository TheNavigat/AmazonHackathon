from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from vivavoce.models import Question

from .forms import UploadFileForm
from .libraries import aws


def index(request):
    User = {}
    User['fullname']= 'Karim ElGhandour'
    Exam = {}
    Exam['name'] = 'Psychology'
    return render(request, 'vivavoce/index.html', {'User': User,'Exam':Exam,})

def start(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'vivavoce/start.html', {
        'question': question,
        'count': Question.objects.count() })

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # TODO: Add else clause and add handling
        if form.is_valid():
            file_name = aws.upload_to_s3(request.FILES['file'].read())
            file_uri = 'https://s3.amazonaws.com/testquestions-8853-5742-7832/' + file_name
            aws.transcribe(file_uri)
            return HttpResponse(status=200)
    return HttpResponse(status=400)


class RecordView(generic.TemplateView):
    template_name = 'vivavoce/record.html'
# Create your views here.
