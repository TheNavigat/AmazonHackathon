from django.db import models


class Question(models.Model):
    s3_name = models.CharField(max_length=200)


class Test(models.Model): pass


class TranscribeJob(models.Model):
    name = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
