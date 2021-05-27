from django.db import models

from carService.models.Category import Category
from carService.models.Product import Product


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
