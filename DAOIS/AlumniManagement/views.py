from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *


@login_required(login_url='Authentication:login')
def dashboard(request):
        
    context = {
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)


def alumni(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, "AlumniManagement/alumni.html", context)


def sample(request):
    jobless_percentage, employed_alumni_percentage, employed_alumni_count = employment_percentage()

    courses_total_count = course_total_students()

    course_analysis = course_related_job_analysis()

    percent_students_list, total_students_list, job_students_list, course_title_list = job_within_six_months()
    combination = zip(percent_students_list, total_students_list, job_students_list, course_title_list)


    alumni_counts = jobs_per_field()
    
    country_data, province_data, city_data, barangay_data = alumni_per_place()
    print(country_data)
    print(province_data)
    print(city_data)
    print(barangay_data)
    context = {
        'jobless_percentage':jobless_percentage,
        'employed_alumni_percentage':employed_alumni_percentage,
        'courses_total_count':courses_total_count,
        'course_analysis': course_analysis,
        'combination': combination,
        'alumni_counts': alumni_counts.to_dict('records'),
    }
    return render(request, 'AlumniManagement/sample.html', context)


