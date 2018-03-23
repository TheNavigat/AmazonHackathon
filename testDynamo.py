import boto3
client = boto3.resource('dynamodb')
table = client.Table('Users')
table.put_item(
   Item={
        'ID' : 1,
        'Name': 'Khadija',
        'image' : 'khadija.jpg'

    }
)

