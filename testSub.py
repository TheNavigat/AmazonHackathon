import boto3
client = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='modelAnswers',
    KeySchema=[
        {
            'AttributeName': 'questionID',
            'KeyType': 'HASH'
        },

    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'questionID',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')

# Print out some data about the table.
print(table.item_count)
