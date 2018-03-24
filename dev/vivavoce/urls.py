from django.urls import path
from . import views

app_name = 'vivavoce'
urlpatterns = [
    path('', views.index, name='index'),
    path('start/<int:question_id>/', views.start, name='start'),
    path('authenticate/', views.authenticate, name='authenicate'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('upload/', views.upload, name='upload'),
    path('rekognize/<int:id>', views.rekognize, name='rekognize'),
    path('thankyou/',views.thankyou,name='thankyou'),

]
