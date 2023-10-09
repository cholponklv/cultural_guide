from django.db import models

# Create your models here.
class Locations(models.Model):
    username = models.CharField(max_length=100,blank=True)