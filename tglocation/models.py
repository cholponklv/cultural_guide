from django.db import models

# Create your models here.
class Locations(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    latitude = models.CharField(max_length=500,blank=True,null=True)
    longitude = models.CharField(max_length=500,blank=True,null=True)

class TgUser(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    latitude = models.CharField(max_length=500,blank=True,null=True)
    longitude = models.CharField(max_length=500,blank=True,null=True)

