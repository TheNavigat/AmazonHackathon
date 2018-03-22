import boto3
translate = boto3.client('translate')
response = translate.translate_text(
    Text='hello',
    SourceLanguageCode='en',
    TargetLanguageCode='ar'
)
print (response)
print (response.get('TranslatedText'))