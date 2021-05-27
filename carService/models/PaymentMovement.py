from django.db import models

from carService.models.PaymentType import PaymentType
from carService.models.CheckingAccount import CheckingAccount
import uuid as uuid


class PaymentMovement(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    checkingAccount = models.ForeignKey(CheckingAccount, on_delete=models.CASCADE, null=True, blank=True)
    paymentAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    paymentType = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True, blank=True)
