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

    similar_job = perform_related_job_analysis(alumni, current_jobs, courses)

    # have job within 6 months upon graduation
    course_bsit = 'BSIT'  # Replace with the desired course ID
    course_bsa = 'BSA'
    num_student_bsit = calculate_num_students_with_job(course_bsit)
    num_student_bsa = calculate_num_students_with_job(course_bsa)

    courses_list = ["BSIT", "BSA"]
    num_students_list = [num_student_bsit, num_student_bsa]  # Add more values if needed

    plt.figure()

    plt.bar(courses_list, num_students_list)
    plt.xlabel('Course')
    plt.ylabel('Number of Students with Job')
    plt.title('Number of Students with Job within 6 Months by Course')

    # Save the plot to a BytesIO object
    plot_buffer = io.BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    encoded_plot = base64.b64encode(plot_buffer.read()).decode('utf-8')

    context = {
        'similar_job': similar_job,
        'encoded_plot': encoded_plot,
        'num_student_bsit': num_student_bsit,
        'num_student_bsa': num_student_bsa
    }

    return render(request, 'AlumniManagement/job.html', context)




