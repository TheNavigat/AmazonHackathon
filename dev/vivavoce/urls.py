from django.urls import path
from . import views

app_name = 'vivavoce'
urlpatterns = [
    path('', views.index, name='index'),
    path('id/', views.id, name='id'),
    path('start/', views.start_init, name='start_init'),
    path('start/<int:test_id>/<int:question_id>/', views.start, name='start'),
    path('authenticate/<int:id>', views.authenticate, name='authenicate'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('rekognize/<int:id>', views.rekognize, name='rekognize'),
    path('upload/<int:test_id>/<int:question_id>/', views.upload, name='upload'),
    path('thankyou/',views.thankyou,name='thankyou'),

]
