import boto3


def upload_to_s3(blob):
    s3 = boto3.resource(
        's3',
        aws_access_key_id='AKIAIO2NRGA6M25NZLYQ',
        aws_secret_access_key='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'
    )

    bucket = s3.Bucket('testquestions-8853-5742-7832')

    count = 0

    for object in bucket.objects.all():
        count += 1

    # s3.Object('testquestions-8853-5742-7832', 'answer' + str(count) + '.wav').put(Body=blob)
