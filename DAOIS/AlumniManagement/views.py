from django.shortcuts import render
from .models import *
from .utils import *
import random

def dashboard(request):
    
    
    course_analysis = course_related_job_analysis()


    total_alumni_count = Alumni_Demographic_Profile.objects.count()
    
    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()
    jobless_percentage, employed_percentage, job_status_pie = create_job_status_chart(total_alumni_count, jobless_alumni_count)


    bar_plot_job_within_6_months, percent_students_list, total_students_list, job_students_list = job_within_six_months_plot()

    course_list = Course.objects.values_list('course_id', flat=True)

    course_percentages = zip(course_list, percent_students_list, total_students_list, job_students_list , [random.choice(['w3-green', 'w3-orange', 'w3-blue', 'w3-red', 'w3-lime', 'w3-brown']) for _ in course_list])

    course_bsit = 'BSIT'  # Replace with the desired course ID
    course_bsa = 'BSA'
    total_students_bsit = calculate_total_students(course_bsit)
    total_students_bsa = calculate_total_students(course_bsa)



    context = {
        'jobless_percentage': jobless_percentage,
        'employed_percentage': employed_percentage,
        'course_percentages': course_percentages,
        'job_status_pie': job_status_pie,
        'total_alumni_count': total_alumni_count,
        'total_students_bsit': total_students_bsit,
        'total_students_bsa': total_students_bsa,
        'course_analysis': course_analysis,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)





def related_job(request):
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    course_analysis = course_related_job_analysis()


    # have job within 6 months upon graduation
    encoded_plot, percent_students_bsit, percent_students_bsa = job_within_six_months_plot()

    context = {
        'course_analysis': course_analysis,
        'encoded_plot': encoded_plot,
    }

    return render(request, 'AlumniManagement/job.html', context)





def alumni(request):
    courses = Course.objects.all()

    context = {
        'courses': courses,
    }
    return render(request, "AlumniManagement/alumni.html", context)