from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    def __str__(self):
        return self.name