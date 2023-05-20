from django.shortcuts import render
from .models import *
from .utils import perform_related_job_analysis


import pandas as pd
import matplotlib.pyplot as plt


from io import BytesIO
import io
import base64


def dashboard(request):
    # alumni_id = "A10002"
    # job_exists = Current_Job.objects.filter(alumni_id=alumni_id).exists()
    # if job_exists:
    # 	print("has a job")
    # else:
    # 	print("No job")

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
    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()

    encoded_plot = perform_related_job_analysis(alumni, current_jobs, courses)

    context = {'encoded_plot': encoded_plot}
    return render(request, 'AlumniManagement/job.html', context)





# def related_job(request):
#     # Fetch the required data from the models
#     alumni = Alumni_Demographic_Profile.objects.all()
#     current_jobs = Current_Job.objects.select_related('alumni').all()
#     courses = Course.objects.all()

#     # Create lists to store the fetched data
#     alumni_data = []
#     current_job_data = []
#     course_data = []

#     # Populate the lists with the fetched data
#     for alum in alumni:
#         alumni_data.append(alum)
#         current_job = current_jobs.filter(alumni=alum).first()
#         current_job_data.append(current_job)
#         course = courses.filter(course_id=alum.course_id_id).first()
#         course_data.append(course)

#     # Create a DataFrame from the fetched data
#     data = {
#         'Alumni': alumni_data,
#         'Current Job': current_job_data,
#         'Course': course_data
#     }
#     df = pd.DataFrame(data)

#     # Perform the analysis
#     df['Job Related to Course'] = df['Course'].apply(lambda x: x.field_type if x else None) == df['Current Job'].apply(lambda x: x.field_type if x else None)

#     # Filtering out None values
#     filtered_jobs = df.dropna(subset=['Job Related to Course'])

#     # Counting related and non-related jobs
#     related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == True].shape[0]
#     non_related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == False].shape[0]

#     # Create the pie chart
#     labels = ['Related to Course', 'Not Related to Course']
#     counts = [related_count, non_related_count]

#     plt.figure(figsize=(8, 6))
#     plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
#     plt.title('Job Related to Course Analysis')

#     # Save the plot to a BytesIO object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     plot_data = buffer.getvalue()
#     buffer.close()

#     # Convert the plot data to a base64 encoded string
#     encoded_plot = base64.b64encode(plot_data).decode('utf-8')

#     # Pass the encoded plot to the template context
#     context = {'encoded_plot': encoded_plot}
#     return render(request, 'AlumniManagement/job.html', context)
