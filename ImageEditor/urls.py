from django.urls import path

from ImageEditor.views import *
from MediaProject import settings

app_name = "ImageEditor"

urlpatterns = {
     path('videoList/', videoList, name='videoList'),
     path('selectVideo/', selectVideo, name="selectVideo"),
     path('selectVideo/<int:pk>', selectVideo, name="selectVideo"),
     path('videoCapture/<int:pk>', videoCapture, name='videoCapture'),
     path('connerClassification/', connerClassification, name='connerClassification'),
     path('imageCrop/', imageCrop, name='imageCrop'),

}

