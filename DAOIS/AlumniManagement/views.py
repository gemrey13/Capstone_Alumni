from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .utils import *
import random


@login_required(login_url='Authentication:login')
def dashboard(request):

    
    

    course_list = Course.objects.values_list('course_id', flat=True)
    course_percentages = zip(course_list, percent_students_list, total_students_list, job_students_list , [random.choice(['w3-green', 'w3-orange', 'w3-blue', 'w3-red', 'w3-lime', 'w3-brown']) for _ in course_list])

    

    context = {
        'course_percentages': course_percentages,
        'job_status_pie': job_status_pie,
        'total_alumni_count': total_alumni_count,
        'total_students_bsit': total_students_bsit,
        'total_students_bsa': total_students_bsa,
        'course_analysis': course_analysis,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)


def alumni(request):
    courses = Course.objects.all()

    context = {
        'courses': courses,
    }
    return render(request, "AlumniManagement/alumni.html", context)


def sample(request):
    
    jobless_percentage, employed_percentage, employed_alumni_count = employment_percentage()


    courses_total_count = course_total_students()

    course_analysis = course_related_job_analysis()

    percent_students_list, total_students_list, job_students_list = job_within_six_months()
    # !!! Continue here!!!!
    # print(percent_students_list)
    # print(total_students_list)
    # print(job_students_list)


    context = {
        'jobless_percentage':jobless_percentage,
        'employed_percentage':employed_percentage,
        'courses_total_count':courses_total_count,
        'course_analysis': course_analysis
    }
    return render(request, 'AlumniManagement/sample.html', context)