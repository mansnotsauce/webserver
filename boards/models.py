from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    img = models.ImageField()
    sop_instance_uid = models.CharField(max_length=64)
    tests = models.CharField(max_length=2)
    results = models.TextField()

