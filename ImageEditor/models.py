from django.db import models

# Create your models here.
from django.db.models import CharField


class VideoList(models.Model):
    title = models.CharField(max_length=50)
    path = models.CharField(max_length=200)
    conner = models.CharField(max_length=5)


class ConnerList(models.Model):
    frame_img = models.ImageField(blank=True, null=True)
    video_title = models.CharField(max_length=50)
    frame_path = models.CharField(max_length=200)
    conner_name = models.CharField(max_length=50)
    conner_start = models.IntegerField()
    conner_last = models.IntegerField()


class ImageCrop(models.Model):
    # path = models.CharField(max_length=255, null=False)

    left = models.IntegerField(null=False)
    top = models.IntegerField(null=False)
    right = models.IntegerField(null=False)
    bottom = models.IntegerField(null=False)


class VideoCapture(models.Model):
    title = models.CharField(max_length=50)
    # media = models.ImageField(null=True, upload_to="")
