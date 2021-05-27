from django.db import models

from carService.models import Product


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.TextField(null=True, blank=True)