from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=45, null=False)
    status = models.CharField(max_length=1, null=False)