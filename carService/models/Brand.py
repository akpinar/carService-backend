from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)