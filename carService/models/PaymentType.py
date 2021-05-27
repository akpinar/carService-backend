from django.db import models


class PaymentType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
