from django import forms
from django.db import models


# Create your models here.

class DataForm(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=1)
    age1 = models.CharField(max_length=1)
    age2 = models.CharField(max_length=1)
    unhurt = models.CharField(max_length=1)
    dead = models.CharField(max_length=1)
    hospitalized = models.CharField(max_length=1)
    hurt_light = models.CharField(max_length=1)
    men = models.CharField(max_length=1)
    women = models.CharField(max_length=1)
    departement = models.CharField(max_length=4)


class DataPred(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    departement = models.CharField(max_length=4)
    age = models.IntegerField()
    gender = models.IntegerField()
    location = models.IntegerField()
    intersection = models.IntegerField()
    light = models.IntegerField()


