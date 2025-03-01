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

class Early_withdrawal(models.Model):
    # signture will be the picture uploaded by the user
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=False, default="")
    # step 1
    step1_option = models.IntegerField() #1 or 2 or 3
    # if select option 2 for step 1, then input the course name
    drop_course1 = models.CharField(max_length=15, default="", blank=True, null=True)
    drop_course2 = models.CharField(max_length=15, default="", blank=True, null=True)
    drop_course3 = models.CharField(max_length=15, default="", blank=True, null=True)

    # step 2
    departure_date = models.DateField()
    step2_option = models.IntegerField() #1 or 2

    # step 3
    step3_option = models.IntegerField() #1 or 2
    # if select option 1 for step 3, then input Date or semester of planned return to the U.S
    return_date = models.DateField(null=True)

    # step 4
    step4_option1 = models.IntegerField() #0 or 1, 0 means no, 1 means yes
    step4_option2 = models.IntegerField() #0 or 1
    step4_option3 = models.IntegerField() #0 or 1

    # step 5
    step5_option1 = models.IntegerField() #0 or 1, 0 means no, 1 means yes
    step5_option2 = models.IntegerField() #0 or 1
    step5_option3 = models.IntegerField() #0 or 1
    step5_option4 = models.IntegerField() #0 or 1, 0 means no, 1 means yes
    step5_option5 = models.IntegerField() #0 or 1

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
