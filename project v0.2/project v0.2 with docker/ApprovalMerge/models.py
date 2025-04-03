from django.db import models

class GraduateStudentPetition(models.Model):
    email = models.CharField(max_length=255, primary_key=True, default="")
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

    name = models.CharField(max_length=255, default="")
    uh_id = models.CharField(max_length=50, default="")
    contact_phone = models.CharField(max_length=20, default="")
    
    PROGRAM_CHOICES = [
        ("ARCH", "Architecture"),
        ("ARTS", "Arts"),
        ("BUSI", "Business"),
        ("EDUC", "Education"),
        ("ENGR", "Engineering"),
        ("HPA", "Health Professions"),
        ("HRM", "Hotel & Restaurant Management"),
        ("LAW", "Law"),
        ("LASS", "Liberal Arts & Social Sciences"),
        ("NSM", "Natural Sciences & Mathematics"),
        ("NURS", "Nursing"),
        ("OPTO", "Optometry"),
        ("PHAR", "Pharmacy"),
        ("SOCW", "Social Work"),
        ("TECH", "Technology"),
    ]
    program = models.CharField(max_length=10, choices=PROGRAM_CHOICES, blank=True)
    
    CAREER_CHOICES = [
        ("Graduate", "Graduate"),
        ("Law", "Law"),
        ("Optometry", "Optometry"),
        ("Pharmacy", "Pharmacy"),
    ]
    career = models.CharField(max_length=20, choices=CAREER_CHOICES, default="")
    
    TERM_CHOICES = [("Spring", "Spring"), ("Fall", "Fall"), ("Summer", "Summer")]
    effective_term = models.CharField(max_length=10, choices=TERM_CHOICES, default="")
    year = models.PositiveIntegerField(default=0)
    
    # Petition Options
    update_program = models.BooleanField(default=False)
    admissions_status = models.BooleanField(default=False)
    add_new_concurrent = models.BooleanField(default=False)
    change_degree_objective = models.BooleanField(default=False)
    degree_requirement_exception = models.BooleanField(default=False)
    leave_of_absence = models.BooleanField(default=False)
    leave_documentation = models.CharField(max_length=255, blank=True, null=True)
    reinstatement = models.BooleanField(default=False)
    late_filing_graduation = models.BooleanField(default=False)
    transfer_credit = models.BooleanField(default=False)
    change_admit_term = models.BooleanField(default=False)
    early_submission = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_explanation = models.TextField(blank=True, null=True)
    
    # Transfer Credit Details
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    city_state_zip = models.CharField(max_length=255, blank=True, null=True)
    hours_transferred = models.PositiveIntegerField(blank=True, null=True)
    transfer_credits = models.PositiveIntegerField(blank=True, null=True)
    catalog_number = models.CharField(max_length=50, blank=True, null=True)
    semester_taken = models.CharField(max_length=50, blank=True, null=True)
    
    explanation = models.TextField(default="")
    # NOTE: Signature saved into /Latex and retrieved based on file name