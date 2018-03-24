from django.urls import path
from . import views

app_name = 'vivavoce'
urlpatterns = [
    path('welcome/<str:name>/', views.index, name='index'),
    path('', views.id, name='id'),
    path('start/', views.start_init, name='start_init'),
    path('start/<int:test_id>/<int:question_id>/', views.start, name='start'),
    path('authenticate/<int:id>/', views.authenticate, name='authenicate'),
    path('record/', views.RecordView.as_view(), name='record'),
    path('rekognize/<int:id>/', views.rekognize, name='rekognize'),
    path('results/<int:test_id>/', views.results, name='results'),
    path('upload/<int:test_id>/<int:question_id>/', views.upload, name='upload'),
    path('thankyou/<int:test_id>/<int:questions_count>/', views.thankyou, name='thankyou'),
]
