import pandas as pd
import matplotlib.pyplot as plt

from datetime import timedelta
from io import BytesIO
import io
import base64

from .models import *

def create_job_status_chart(total_alumni_count, jobless_alumni_count):
    employed_alumni_count = total_alumni_count - jobless_alumni_count

    # Calculate the percentages
    jobless_percentage = (jobless_alumni_count / total_alumni_count) * 100
    employed_percentage = 100 - jobless_percentage

    # Create the pie chart
    labels = ['Jobless Alumni', 'Employed Alumni']
    sizes = [jobless_percentage, employed_percentage]
    explode = (0.1, 0)  # Explode the 'Jobless Alumni' slice
    colors = ['#ff9999', '#66b3ff']
    plt.figure()
    plt.pie(sizes, shadow=True,explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Alumni Job Status')

    # Convert the plot to an image for rendering in the template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return jobless_percentage, employed_percentage, image_base64


def perform_related_job_analysis(alumni, current_jobs, courses):
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

    # Filtering out None values
    filtered_jobs = df.dropna(subset=['Job Related to Course'])

    # Counting related and non-related jobs
    related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == True].shape[0]
    non_related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == False].shape[0]

    # Create the pie chart
    labels = ['Related to Course', 'Not Related to Course']
    counts = [related_count, non_related_count]

    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=50)
    plt.title('Job Related to Course Analysis')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = buffer.getvalue()
    buffer.close()

    # Convert the plot data to a base64 encoded string
    encoded_plot = base64.b64encode(plot_data).decode('utf-8')

    return encoded_plot


def calculate_num_students_with_job(course_id):
    # Fetch data from Django models and create DataFrames
    alumni_data = list(Alumni_Demographic_Profile.objects.all().values())
    current_job_data = list(Current_Job.objects.all().values())
    graduate_data = list(Graduate.objects.all().values())

    alumni_df = pd.DataFrame(alumni_data)
    current_job_df = pd.DataFrame(current_job_data)
    graduate_df = pd.DataFrame(graduate_data)

    # Merge alumni_df and graduate_df on alumni_id
    merged_df = pd.merge(alumni_df, graduate_df, left_on='alumni_id', right_on='alumni_id_id')

    # Calculate the date six months after graduation
    merged_df['graduation_date'] = pd.to_datetime(merged_df['graduation_date'])
    merged_df['six_months_after_graduation'] = merged_df['graduation_date'] + timedelta(days=180)

    # Merge with current_job_df on alumni_id and filter by specific course
    filtered_df = pd.merge(merged_df, current_job_df, left_on='alumni_id', right_on='alumni_id')
    filtered_df = filtered_df[filtered_df['course_id_id'] == course_id]

    # Filter the students with a job within six months of graduation
    filtered_df = filtered_df[filtered_df['start_date'] <= filtered_df['six_months_after_graduation']]

    # Count the number of students
    num_students_with_job_within_six_months = len(filtered_df)

    return num_students_with_job_within_six_months


def calculate_total_students(course_id):
    total_students = Alumni_Demographic_Profile.objects.filter(course_id=course_id).count()
    return total_students if total_students > 0 else 0


def job_within_six_months_plot():
    course_bsit = 'BSIT'  # Replace with the desired course ID
    course_bsa = 'BSA'

    total_students_bsit = calculate_total_students(course_bsit)
    total_students_bsa = calculate_total_students(course_bsa)

    job_students_bsit = calculate_num_students_with_job(course_bsit)
    job_students_bsa = calculate_num_students_with_job(course_bsa)

    percent_students_bsit = (job_students_bsit / total_students_bsit) * 100 if total_students_bsit != 0 else 0
    percent_students_bsa = (job_students_bsa / total_students_bsa) * 100 if total_students_bsa != 0 else 0

    courses_list = ["BSIT", "BSA"]
    num_students_list = [job_students_bsit, job_students_bsa]  # Add more values if needed

    plt.figure()

    plt.bar(courses_list, num_students_list)
    plt.xlabel('Course')
    plt.ylabel('Number of Students with Job')
    plt.title('Percentage of Graduate Students with Job within 6 Months by Course')

    # Save the plot to a BytesIO object
    plot_buffer = io.BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    encoded_plot = base64.b64encode(plot_buffer.read()).decode('utf-8')

    return encoded_plot, percent_students_bsit, percent_students_bsa