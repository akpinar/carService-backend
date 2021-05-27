import uuid as uuid
from django.db import models

from carService.models import CheckingAccount


class Installment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    checkingAccount = models.ForeignKey(CheckingAccount, on_delete=models.CASCADE, null=True, blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    isPayed = models.BooleanField(default=False)
    paymentAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paymentDate = models.DateField(blank=True, null=True)
