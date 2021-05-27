import uuid as uuid
from django.db import models

from carService.models import Profile
from carService.models.Camera import Camera
from carService.models.Car import Car
from carService.models.ServiceType import ServiceType


class Service(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    serviceKM = models.IntegerField(null=True, blank=True)
    isOrder = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    serviceType = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    complaint = models.CharField(max_length=500, blank=True, null=True)
    responsiblePerson = models.CharField(max_length=100, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
