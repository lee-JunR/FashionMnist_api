from rest_framework import routers
from django.urls import path, include
from .views import index, MyFileView,test
from . import views
app_name = 'mnistapp'

urlpatterns = [
    path('', index, name='home'),
    path('predict/',MyFileView.as_view()),
]

