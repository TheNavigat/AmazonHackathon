from django.contrib import admin
from .models import Question, TranscribeJob


admin.site.register(Question)
admin.site.register(TranscribeJob)

# Register your models here.
