from django.urls import path

from ImageEditor.views import *
from MediaProject import settings

app_name = "ImageEditor"

urlpatterns = {
     path('videoList/', videoList, name='videoList'),
     path('selectVideo/<int:id>', selectVideo, name="selectVideo"),
     path('imageCrop/', imageCrop, name='imageCrop'),
}

