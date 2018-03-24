import boto3
questions= ["what is meant by the term latent heat?",
            "Explain the energy changes undergone by the molecules of a substance during the period when latent heat of vaporization is being supplied?",
            "State one way in which energy is lost from the transformer, and from which part it is lost.",
            "State two things which could be done to increase the speed of rotation of the coil.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle."
            ]
dynamodb = boto3.resource('dynamodb')
modelAnswersTable = dynamodb.Table('modelAnswers')
userAnswersTable = dynamodb.Table('userAnswers')

givenAnswer = ["It is the energy required to change the state of an object from one state to the other with no change in temperature in between the states.",
        "The energy is used to change the substance from liquid to vapour by overcoming the intermolecular forces.",
        "Energy is lost as heat energy in the coil.",
        "It is possible to do two things, more voltage and more current.",
        "Beta waves are deflected more than alpha waves. The deflections are in opposite directions. The paths are curves.",
        "Beta waves are deflected more than alpha waves. The deflections are in opposite directions. The paths are curves."]

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
print('Calling DetectKeyPhrases')
givenAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=givenAnswer, LanguageCode="en")['ResultList']
# givenAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=givenAnswer, LanguageCode="en")['ResultList']
bigset=[]
for i in range(0,6): #answer
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

# Matching algorithm
for i in range(1,7): #each one of the whole answer
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
    userAnswersTable.put_item(
        Item={
            'questionID': i,
            'Score': score,

        }
    )
    accScore+=score

print("final score is" )
print((accScore/600)*100 )
######## api thing
def getScore():

    check = userAnswersTable.get_item(Key={'questionID': 1,})
    try:
        check['Item']
    except Exception as e:
        return -1
    scoreAcc=0
    for i in range(1,7):
        givenAnswer = userAnswersTable.get_item(
            Key={
                'questionID': i,
            }
        )
        scoreValue= givenAnswer['Item']['Score']
        if(scoreValue is  None):
            return -1
        else:
            scoreAcc+=scoreValue

    return (scoreAcc/600)*100
x= getScore()
print(x)

