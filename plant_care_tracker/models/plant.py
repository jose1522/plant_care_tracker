from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
