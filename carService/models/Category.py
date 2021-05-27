from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)
