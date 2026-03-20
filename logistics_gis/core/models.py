from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    status = models.CharField(max_length=50, default="pending")

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name
    