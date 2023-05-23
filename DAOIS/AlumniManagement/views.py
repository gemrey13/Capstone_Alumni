from django.shortcuts import render
from .models import *
from .utils import *
import pandas as pd
from datetime import datetime, timedelta


def dashboard(request):
    
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    total_alumni_count = Alumni_Demographic_Profile.objects.count()
    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()

    jobless_percentage, employed_percentage, image_base64 = create_job_status_chart(total_alumni_count, jobless_alumni_count)


    encoded_plot, percent_students_bsit, percent_students_bsa = job_within_six_months_plot()

    course_bsit = 'BSIT'  # Replace with the desired course ID
    course_bsa = 'BSA'

    total_students_bsit = calculate_total_students(course_bsit)
    total_students_bsa = calculate_total_students(course_bsa)

    course_analysis = perform_related_job_analysis(alumni, current_jobs, courses)

    context = {
        'jobless_percentage': jobless_percentage,
        'employed_percentage': employed_percentage,
        'image_base64': image_base64,
        'total_alumni_count': total_alumni_count,
        'percent_students_bsit': percent_students_bsit,
        'total_students_bsit': total_students_bsit,
        'percent_students_bsa': percent_students_bsa,
        'total_students_bsa': total_students_bsa,
        'course_analysis': course_analysis,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)


def related_job(request):
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    course_analysis = perform_related_job_analysis(alumni, current_jobs, courses)


    # have job within 6 months upon graduation
    encoded_plot, percent_students_bsit, percent_students_bsa = job_within_six_months_plot()

    context = {
        'course_analysis': course_analysis,
        'encoded_plot': encoded_plot,
        'percent_students_bsit': percent_students_bsit,
        'percent_students_bsa': percent_students_bsa
    }

    return render(request, 'AlumniManagement/job.html', context)


