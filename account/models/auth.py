from django.db import models
from . import user as user_models
class SecondLevelDatabase(models.Model):
    """
    this saves the excel file of the Lumni which contains all members details..
    """
    data = models.JSONField(null=True)


class Chapters(models.Model):
    name = models.CharField(max_length=300,null=True)
    user  = models.ManyToManyField('User')


    def __str__(self): return self.name