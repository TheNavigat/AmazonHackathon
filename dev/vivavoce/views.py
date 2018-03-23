from .models import Question
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .forms import UploadFileForm
import boto3
from boto3.dynamodb.conditions import Key, Attr
from binascii import a2b_base64
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

def thankyou(request):
    return render(request, 'vivavoce/thankyou.html')
    
def authenticate(request):
    return render(request, 'vivavoce/basic.html')

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

def rekognize(path, id):
    a,data= path.split(",")
    binary_data = a2b_base64(data)

    fd = open('image.png', 'wb')
    fd.write(binary_data)
    fd.close()

    rekognition = boto3.client('rekognition')
    table = boto3.resource('dynamodb').Table('Users')
    src  = table.query(
        KeyConditionExpression=Key('ID').eq(id)
    )
    image=src['Items'][0]['image']
    print(image)
    compareImagefile='image.png'
    compareImage= open(compareImagefile,'rb')
    response = rekognition.compare_faces(
            SimilarityThreshold=70,
            SourceImage = {
                'S3Object': {
                    'Bucket': 'testquestions-8853-5742-7832',
                    'Name': image,
                }
            },
            TargetImage = {
                'Bytes': compareImage.read()
        }
    )
    if not not response['FaceMatches']:
        return redirect('index');

class RecordView(generic.TemplateView):
    template_name = 'vivavoce/record.html'
# Create your views here.
