from django.urls import path
from . import views

app_name = 'vivavoce'
urlpatterns = [
    path('', views.index, name='index'),
    path('record/', views.RecordView.as_view(), name='record'),
]
