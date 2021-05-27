from django.db import models
import uuid as uuid

from carService.models.Profile import Profile


class Car(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    plate = models.CharField(max_length=200, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    brand = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    engine = models.CharField(max_length=200, blank=True, null=True)
    oilType = models.CharField(max_length=200, blank=True, null=True)
    chassisNumber = models.CharField(max_length=200, null=True, blank=True)
    currentKM = models.IntegerField(null=True, blank=True)
    engineNumber = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=255, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    isDeleted = models.BooleanField(default=False)
