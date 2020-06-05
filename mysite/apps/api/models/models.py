from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=128, unique=True)
    pw = models.CharField(max_length=128)
    type = models.CharField(max_length=5)
    

class Request(models.Model):
    status = models.CharField(max_length=5)
    from_addr = models.CharField(max_length=128)
    to_addr = models.CharField(max_length=128)
    user_id = models.IntegerField()
    driver_id = models.IntegerField(null=True,)
    requested = models.DateTimeField(auto_now=False, auto_now_add=True)
    assigned = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,)
    canceled = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,)