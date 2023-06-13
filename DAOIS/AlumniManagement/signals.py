from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Current_Job, Previous_Job
from datetime import date

@receiver(pre_delete, sender=Current_Job)
def move_to_previous_job(sender, instance, **kwargs):
    previous_job = Previous_Job(
        previous_job_id=instance.current_job_id,
        job_title=instance.job_title,
        salary=instance.salary,
        start_date=instance.start_date,
        end_date=date.today(),
        company_name=instance.company_name,
        alumni=instance.alumni,
        country=instance.country,
        province=instance.province,
        city=instance.city,
        barangay=instance.barangay
    )
    previous_job.save()
