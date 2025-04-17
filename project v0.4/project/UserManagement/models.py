from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=45, null=False)
    status = models.CharField(max_length=1, null=False)
    level1 = models.CharField(max_length=1, null=False, default='0')
    level2 = models.CharField(max_length=1, null=False, default='0')
    cougarID = models.IntegerField(null=True)

class Delegate(models.Model):
    delegateId = models.AutoField(primary_key=True)
    delegateUserEmail = models.CharField(max_length=255)
    delegateFormName = models.CharField(max_length=255)
    delegateTo = models.CharField(max_length=255)

class Workflow(models.Model):
    form_name = models.CharField(max_length=255, primary_key=True)
    Level = models.CharField(max_length=1, null=False, default='2')