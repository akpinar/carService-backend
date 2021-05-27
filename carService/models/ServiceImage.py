from django.db import models

from carService.models import Service


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    image = models.TextField(null=True, blank=True)