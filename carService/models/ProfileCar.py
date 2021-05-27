from django.db import models

from carService.models.Car import Car
from carService.models.Profile import Profile


class ProfileCar(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
