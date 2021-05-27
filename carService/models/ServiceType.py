from django.db import models


class ServiceType(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
