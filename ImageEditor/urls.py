from django.urls import path

from ImageEditor.views import *
from MediaProject import settings

app_name = "ImageEditor"

urlpatterns = {
     path('videoList/', videoList, name='videoList'),
     path('selectVideo/<int:pk>', selectVideo, name="selectVideo"),
     path('selectVideo/', selectVideo, name="selectVideo_post"),
     path('imageCrop/', imageCrop, name='imageCrop'),

}

