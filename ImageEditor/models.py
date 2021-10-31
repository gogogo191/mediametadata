from django.db import models

# Create your models here.
from django.db.models import CharField


class Video(models.Model):
    id = models.BigAutoField(help_text="Video ID", primary_key=True)
    title = models.CharField(help_text="Video Title", max_length=50, blank=False, null=False)
    path = models.CharField(help_text="Video Path", max_length=200, blank=False, null=False)
    conner = models.CharField(help_text="Conner Existence", max_length=5, default="N")


class Conner(models.Model):
    id = models.BigAutoField(help_text="Conner ID", primary_key=True)
    frame_img = models.TextField(help_text="Conner Representative Image", blank=True, null=True)
    video_id = models.IntegerField(help_text="Video_id")
    conner_name = models.CharField(help_text="Conner Name", max_length=50)
    conner_start = models.IntegerField(help_text="Conner Start")
    conner_end = models.IntegerField(help_text="Conner End")

