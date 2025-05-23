from django.db import models

# Create your models here.
class Public_info(models.Model):
    # signture will be the picture uploaded by the user
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False, default="")
    option = models.CharField(max_length=1) # 'A' or 'B'
    ID = models.CharField(max_length=10)
    date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[("draft", "raft"),
                 ("pending", "pending"),
                 ("returned", "returned"),
                 ("approved", "approved"),],
        default="draft"
    )
    note = models.CharField(max_length=255, default="", blank=True, null=True)
    level1 = models.CharField(max_length=1, null=False, default='0')
    level2 = models.CharField(max_length=1, null=False, default='0')

class Early_withdrawal(models.Model):
    # signture will be the picture uploaded by the user
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False, default="")
    # step 1
    step1_option = models.CharField(max_length=1) #'1' or '2' or '3'
    # if select option 2 for step 1, then input the course name
    drop_course1 = models.CharField(max_length=15, default="", blank=True, null=True)
    drop_course2 = models.CharField(max_length=15, default="", blank=True, null=True)
    drop_course3 = models.CharField(max_length=15, default="", blank=True, null=True)

    # step 2
    departure_date = models.DateField()
    step2_option = models.CharField(max_length=1) #'1' or '2'

    # step 3
    step3_option = models.CharField(max_length=1) #1 or 2
    # if select option 1 for step 3, then input Date or semester of planned return to the U.S
    return_date = models.DateField(null=True)

    ID = models.CharField(max_length=10)
    date = models.DateTimeField()
    
    status = models.CharField(
        max_length=20,
        choices=[("draft", "draft"),
                 ("pending", "pending"),
                 ("returned", "returned"),
                 ("approved", "approved"),],
        default="draft"
    )
    note = models.CharField(max_length=255, default="", blank=True, null=True)
    level1 = models.CharField(max_length=1, null=False, default='0')
    level2 = models.CharField(max_length=1, null=False, default='0')


class Graduate_petition(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    level1 = models.CharField(max_length=1, null=False, default='0')
    level2 = models.CharField(max_length=1, null=False, default='0')


class Undergraduate_transfer(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    level1 = models.CharField(max_length=1, null=False, default='0')
    level2 = models.CharField(max_length=1, null=False, default='0')

class Historical_approval(models.Model):
    approval_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255)
    locatedFolder = models.CharField(max_length=255, null=True)