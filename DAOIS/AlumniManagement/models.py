from django.db import models

FIELD_CHOICES = [
        ('technology', 'Technology'),
        ('medical', 'Medical/Healthcare'),
        ('mechanical', 'Mechanical Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('finance', 'Finance/Accounting'),
        ('education', 'Education/Teaching'),
        ('marketing', 'Marketing/Advertising'),
        ('sales', 'Sales'),
        ('business', 'Business Development'),
        ('hr', 'Human Resources'),
        ('law', 'Law/Legal'),
        ('consulting', 'Consulting'),
        ('manufacturing', 'Manufacturing'),
        ('hospitality', 'Hospitality/Travel'),
        ('retail', 'Retail'),
        ('media', 'Media/Entertainment'),
        ('art', 'Art/Design'),
        ('architecture', 'Architecture'),
        ('nonprofit', 'Nonprofit/Volunteering'),
        ('government', 'Government/Public Administration'),
    ]


class Course(models.Model):
    course_id = models.CharField(max_length=6, primary_key=True)
    course_name = models.CharField(max_length=64, blank=False)
    course_desc = models.CharField(max_length=255, blank=True)
    field_type = models.CharField(max_length=64, choices=FIELD_CHOICES, default='technology')

    def __str__(self):
        return f'{self.course_id}'

class Alumni_Demographic_Profile(models.Model):
    alumni_id = models.CharField(primary_key=True, max_length=6)
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    mi = models.CharField(max_length=2, blank=True)
    suffix = models.CharField(max_length=3, blank=True)

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=64)
    religion = models.CharField(max_length=64)
    marital_status = models.CharField(max_length=64)
    date_of_birth = models.CharField(max_length=64)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, default='BSIT')

    def __str__(self):
        return f'{self.fname} {self.lname}'

class Current_Job(models.Model):
    current_job_id = models.CharField(primary_key=True, max_length=6)
    field_type = models.CharField(max_length=64, choices=FIELD_CHOICES, default='technology')
    job_title = models.CharField(max_length=64)
    salary = models.IntegerField()
    start_date = models.DateField()
    company_name = models.CharField(max_length=64)
    company_address = models.CharField(max_length=64)
    alumni = models.ForeignKey(Alumni_Demographic_Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.job_title

class Previous_Job(models.Model):
    previous_job_id = models.CharField(primary_key=True, max_length=10)
    job_title = models.CharField(max_length=64)
    salary = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    company_name = models.CharField(max_length=64)
    company_address = models.CharField(max_length=64)
    alumni = models.ForeignKey(Alumni_Demographic_Profile, on_delete=models.CASCADE, null=True, blank=True)


class Curriculum(models.Model):
    curriculum_id = models.CharField(max_length=6, primary_key=True)
    curriculum_name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=4, blank=False)

    def __str__(self):
        return self.curriculum_name


class Segment(models.Model):
    segment_id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    current_job = models.ForeignKey(Current_Job, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)



class Graduate(models.Model):
    graduate_id = models.CharField(max_length=6, primary_key=True)
    graduation_date = models.DateField()
    degree = models.CharField(max_length=64)
    honor = models.CharField(max_length=64)

class Educational_Attainment(models.Model):
    alumni_id = models.ForeignKey(Alumni_Demographic_Profile, on_delete=models.CASCADE)
    graduate_id = models.ForeignKey(Graduate, on_delete=models.CASCADE)
    

