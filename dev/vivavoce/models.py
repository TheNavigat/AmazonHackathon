from django.db import models

class Question(models.Model):
    s3_name = models.CharField(max_length=200)
