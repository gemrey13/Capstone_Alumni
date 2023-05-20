from django.shortcuts import render
from .models import *

import pandas as pd
import matplotlib.pyplot as plt

import io
import base64


def dashboard(request):
    alumni_id = "A10002"
    job_exists = Current_Job.objects.filter(alumni_id=alumni_id).exists()
    if job_exists:
    	print("has a job")
    else:
    	print("No job")

    total_alumni_count = Alumni_Demographic_Profile.objects.count()

    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()
    employed_alumni_count = total_alumni_count - jobless_alumni_count

    # Calculate the percentages
    jobless_percentage = (jobless_alumni_count / total_alumni_count) * 100
    employed_percentage = 100 - jobless_percentage

    # Create the pie chart
    labels = ['Jobless Alumni', 'Employed Alumni']
    sizes = [jobless_percentage, employed_percentage]
    explode = (0.1, 0)  # Explode the 'Jobless Alumni' slice
    colors = ['#ff9999', '#66b3ff']
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Alumni Job Status')

    # Convert the plot to an image for rendering in the template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    context = {
        'jobless_percentage': jobless_percentage,
        'image_base64': image_base64,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)


def related_job(request):
	# Fetch the required data from the models
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    # Create lists to store the fetched data
    alumni_data = []
    current_job_data = []
    course_data = []

    # Populate the lists with the fetched data
    for alum in alumni:
        alumni_data.append(alum)
        current_job = current_jobs.filter(alumni=alum).first()
        current_job_data.append(current_job)
        course = courses.filter(course_id=alum.course_id_id).first()
        course_data.append(course)

    # Create a DataFrame from the fetched data
    data = {
        'Alumni': alumni_data,
        'Current Job': current_job_data,
        'Course': course_data
    }
    df = pd.DataFrame(data)

    # Perform the analysis
    df['Job Related to Course'] = df['Course'].apply(lambda x: x.field_type if x else None) == df['Current Job'].apply(lambda x: x.field_type if x else None)

    # Convert the DataFrame to HTML
    html_table = df.to_html(classes='table')

    # Pass the HTML table to the template context
    context = {'html_table': html_table}
    return render(request, 'AlumniManagement/job.html', context)

	
    
   