import boto3
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
text = ["It is the energy required to change the state of an object from one state to the other with no change in temperature in between the states.",
        "The energy is used to change the substance from liquid to vapour by overcoming the intermolecular forces.",
        "Energy is lost as heat energy in coil.", "It is possible to do to things, more voltage and more current.",
        "Beta waves are deflected more than alpha waves. The deflections are in opposite directions. The paths are curves."]
print('Calling DetectKeyPhrases')
result = comprehend.batch_detect_key_phrases(TextList=text, LanguageCode="en")['ResultList']
set = []
for object in result[4]['KeyPhrases']:
    set.append(object['Text'])
print(set)
print('End of DetectKeyPhrases\n')
