from django.shortcuts import render
from .models import *
from .utils import *
import pandas as pd
from datetime import datetime, timedelta


def dashboard(request):
    total_alumni_count = Alumni_Demographic_Profile.objects.count()
    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()

    jobless_percentage, employed_percentage, image_base64 = create_job_status_chart(total_alumni_count, jobless_alumni_count)

    context = {
        'jobless_percentage': jobless_percentage,
        'employed_percentage': employed_percentage,
        'image_base64': image_base64,
        'total_alumni_count': total_alumni_count,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)


def related_job(request):
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    encoded_plot = perform_related_job_analysis(alumni, current_jobs, courses)

    
    course_id = 'BSIT'  # Replace with the desired course ID
    num_students = calculate_num_students_with_job(course_id)

    context = {
        'encoded_plot': encoded_plot,
        'num_students': num_students
    }

    return render(request, 'AlumniManagement/job.html', context)




