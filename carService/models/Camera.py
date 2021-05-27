from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255,blank=True, null=True)