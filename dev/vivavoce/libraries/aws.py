import boto3
import time
import urllib.request
import json

from vivavoce.models import TranscribeJob


AWS_ACCESS_KEY = 'AKIAIO2NRGA6M25NZLYQ'
AWS_SECRET_ACCESS_KEY = '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'

def transcribeFiles(quiz, questions):
    transcribe = boto3.client('transcribe')
    givenAnswer = []
    i = 1
    while i <= questions:
        transcribe.start_transcription_job(
        TranscriptionJobName=str(quiz)+'-'+str(i),
        Media={'MediaFileUri': "https://s3.amazonaws.com/testquestions-8853-5742-7832/" + str(quiz) + "-" + str(i) + ".wav"},
        MediaFormat='wav',
        LanguageCode='en-US',
        MediaSampleRateHertz=44100
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=str(quiz)+'-'+str(i))
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print(i)
            time.sleep(5)
        url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = urllib.request.urlopen(url)
        data = response.read()
        text = data.decode('utf-8')
        d = json.loads(text)
        string = ''
        for sent in d['results']['transcripts']:
            string+=(sent['transcript'])
        givenAnswer.append(string)
        i = i + 1

    print(givenAnswer)

    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    print('Calling DetectKeyPhrases')
    givenAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=givenAnswer, LanguageCode="en")['ResultList']
    # givenAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=givenAnswer, LanguageCode="en")['ResultList']
    bigset=[]
    for i in range(0, questions): #answer
        answer=[]
        set=[]
        for object in givenAnswerPhrases[i]['KeyPhrases']: #phrases
            answer = object['Text']
            x = answer.split(" ")
            outputAnswer = ''

            for j in range(0,len(x)):#each phrase
                tempAnswer=x[j]
                if tempAnswer=='the':
                    tempAnswer =''
                if tempAnswer=='The':
                    tempAnswer =''
                if tempAnswer=='a':
                    tempAnswer =''
                if tempAnswer=='A':
                    tempAnswer =''
                if tempAnswer=='an':
                    tempAnswer =''
                if tempAnswer == 'An':
                    tempAnswer = ''
                if (tempAnswer!='') :
                    outputAnswer+=tempAnswer+" "
            set.append(outputAnswer)
        bigset.append(set)
    # for k in range(0, 6):
    #     currentAnswer = bigset[k]
    #     print(currentAnswer)

    accScore = 0

    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # Matching algorithm
    modelAnswersTable = dynamodb.Table('modelAnswers')

    for i in range(1, questions + 1): #each one of the whole answer
        modelAnswer = modelAnswersTable.get_item(
            Key={
                'questionID': i,
            }
        )

        currentAnswer = bigset[i-1]
        print(currentAnswer)
        modelAnswerLength = len(modelAnswer['Item']['answer'])
        score= 0
        for j in range(0,modelAnswerLength): #each phrase
            item1 = modelAnswer['Item']['answer'][j]
            weightValue = modelAnswer['Item']['weight'][j]
            isRequired= modelAnswer['Item']['required'][j]
            found = False
            for l in range(0,len(currentAnswer)):

                if((currentAnswer[l].lower()).find(item1.lower())==0 ):
                    score+=weightValue
                    found=True

            if(found==False and isRequired== True):
                score=0
                break
        print(score)
        userAnswersTable = dynamodb.Table('userAnswers')
        userAnswersTable.put_item(
            Item={
                'testID': quiz,
                'questionID': i,
                'Score': score,

            }
        )

def transcribe(answer_uri, job_name):
    transcribe = boto3.client('transcribe')

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': answer_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        MediaSampleRateHertz=22050
    )

    t = TranscribeJob(name=job_name, status="In Progress")
    t.save()

def upload_to_s3(test_id, question_id, blob):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    file_name = str(test_id) + '-' + str(question_id) + '.wav'

    s3.Object(
        'testquestions-8853-5742-7832', file_name
    ).put(ACL='public-read', Body=blob)

    return file_name

def getScore(test_id):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    userAnswersTable = dynamodb.Table('userAnswers')
    check = userAnswersTable.get_item(Key={'questionID': 1, 'testID': test_id,})

    try:
        check['Item']
    except Exception as e:
        return -1
    scoreAcc=0
    for i in range(1,7):
        givenAnswer = userAnswersTable.get_item(
            Key={
                'questionID': i,
                'testID': test_id,
            }
        )
        scoreValue= givenAnswer['Item']['Score']
        if(scoreValue is  None):
            return -1
        else:
            scoreAcc+=scoreValue

    return (scoreAcc/600)*100
