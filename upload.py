import boto3


def upload(path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('mybucket')
    count = 0
    for object in bucket.objects.all():
        count += 1
    s3.Object('testquestions-8853-5742-7832', 'answer'+str(count)+'.mp3').put(Body=open(path, 'rb'))
