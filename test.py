import boto3
questions= ["what is meant by the term latent heat?",
            "Explain the energy changes undergone by the molecules of a substance during the period when latent heat of vaporization is being supplied?",
            "State one way in which energy is lost from the transformer, and from which part it is lost.",
            "State two things which could be done to increase the speed of rotation of the coil.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle.",
            "A beam of αlpha particles and Beta particles passes, in a vacuum, between the poles of a strong magnet. Compare the deflections of the paths of the two types of particle."
            ]

modelAnswer = ["It is the energy required to change the state of an object from one state to the other with no change in temperature in between the states.",
        "The energy is used to change the substance from liquid to vapour by overcoming the intermolecular forces.",
        "Energy is lost as heat energy in coil.",
        "It is possible to do two things, more voltage and more current.",
        "Beta waves are deflected more than alpha waves. The deflections are in opposite directions. The paths are curves.",
        "Beta waves are deflected more than alpha waves. The deflections are in opposite directions. The paths are curves."]
givenAnswer=[]

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
print('Calling DetectKeyPhrases')
modelAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=modelAnswer, LanguageCode="en")['ResultList']
# givenAnswerPhrases = comprehend.batch_detect_key_phrases(TextList=givenAnswer, LanguageCode="en")['ResultList']
bigset=[]
for i in range(0,6): #answer
    answer=[]
    set=[]
    for object in modelAnswerPhrases[i]['KeyPhrases']: #phrases
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
print(bigset)
answer1 =[ 'energy', 'state', 'object', 'one state', 'other', 'no change', 'temperature', 'states']
weight1= [20,10,5,10,5,5,20,20,5]
required1=[True,False,False,False,False,True,True,False]
answer2 =['energy ', 'substance ', 'liquid ', 'vapour ', 'intermolecular forces ']
weight2= [20,10,10,10,50]
required2=[True,False,True,False,True]
answer3 =['Energy', 'heat energy', 'coil']
weight3= [5,80,15]
required3=[False,True,True]
answer4 =[ 'two things ', 'more voltage ', 'more current ']
weight4= [0,50,50]
required4=[False,True,True]
answer5 =['Beta waves', 'more than alpha waves', 'The deflections', 'opposite directions', 'The paths', 'curves']
weight5= [25,25,25,25,25,25]
required5=[False,False,False,False,False,False,False,False]
answer6 =['Beta waves', 'more than alpha waves', 'The deflections', 'opposite directions', 'The paths', 'curves']
weight6= [25,25,25,25,25,25]
required6=[False,False,False,False,False,False,False,False]

print('End of DetectKeyPhrases\n')
table = dynamodb.Table('modelAnswers')

for i in range(0,6): #answer
    response = table.get_item(
        Key={
            'questionID': i,
        }
    )
    item1 = response['Item']['answer'][i]
    item2 = response['Item']['weight'][i]
    item3= response['Item']['required'][i]
    print(item1 +" "+item2+" "+item3)