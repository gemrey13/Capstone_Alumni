from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=6, primary_key=True)
    course_name = models.CharField(max_length=64, blank=False)
    course_desc = models.CharField(max_length=255, blank=True)

class Current_Job(models.Model):
    current_job_id = models.CharField(primary_key=True, max_length=10)
    job_title = models.CharField(max_length=64)
    salary = models.IntegerField()
    start_date = models.DateField()
    company_name = models.CharField(max_length=64)
    company_address = models.CharField(max_length=64)

class Curriculum(models.Model):
    curriculum_id = models.CharField(max_length=10, primary_key=True)
    curriculum_name = models.CharField(max_length=64, blank=False)
    description = models.CharField(max_length=255, blank=True)
    year = models.DateField(blank=False)

class Segment(models.Model):
    segment_id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    current_job = models.ForeignKey(Current_Job, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

class Previous_Job(models.Model):
    previous_job_id = models.CharField(primary_key=True, max_length=10)
    job_title = models.CharField(max_length=64)
    salary = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    company_name = models.CharField(max_length=64)
    company_address = models.CharField(max_length=64)

class Alumni_Demographic_Profile(models.Model):
    alumni_id = models.CharField(primary_key=True, max_length=10)
    fname = models.CharField(max_length=64)
    lname = models.CharField(max_length=64)
    mi = models.CharField(max_length=2)
    suffix = models.CharField(max_length=3)
    address = models.CharField(max_length=64)
    religion = models.CharField(max_length=64)
    marital_status = models.CharField(max_length=64)
    date_of_birth = models.CharField(max_length=64)
    current_job = models.ForeignKey(Current_Job, on_delete=models.SET_NULL, null=True, blank=True)
    previous_job = models.ForeignKey(Previous_Job, on_delete=models.SET_NULL, null=True, blank=True)

class Graduate(models.Model):
    graduate_id = models.CharField(max_length=10, primary_key=True)
    graduation_date = models.DateField()
    degree = models.CharField(max_length=64)
    honor = models.CharField(max_length=64)

class Educational_Attainment(models.Model):
    alumni_id = models.ForeignKey(Alumni_Demographic_Profile, on_delete=models.CASCADE)
    graduate_id = models.ForeignKey(Graduate, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

