from django.urls import path
from . import views

app_name = 'vivavoce'
urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start, name='start'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('upload/', views.upload, name='upload'),
    path('rekognize/', views.rekognize, name='rekognize'),
]

