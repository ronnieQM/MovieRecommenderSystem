from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    name = models.CharField(max_length=30, unique=False)
    description = models.CharField(max_length=300)
    release_date = models.DateField()
    img = models.CharField(max_length=100)
    runtime = models.IntegerField()
    release_country = models.CharField(max_length=5)
    dbo = models.IntegerField()
    revenue = models.IntegerField()



    def __str__(self):
        return self.name

class Actor(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Director(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Genres(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Reviews(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


