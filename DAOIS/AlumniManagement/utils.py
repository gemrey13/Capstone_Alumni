import pandas as pd
import matplotlib.pyplot as plt

from datetime import timedelta
from io import BytesIO
import io
import base64

from django.db.models import Count, F
from .models import *



def employment_percentage():
    total_alumni_count = Alumni_Demographic_Profile.objects.count()
    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()

    employed_alumni_count = total_alumni_count - jobless_alumni_count

    # Calculate the percentages
    jobless_percentage = (jobless_alumni_count / total_alumni_count) * 100
    employed_percentage = 100 - jobless_percentage


    return jobless_percentage, employed_percentage, employed_alumni_count



def course_related_job_analysis():

    alumni = Alumni_Demographic_Profile.objects.all()
    current_jobs = Current_Job.objects.select_related('alumni').all()
    courses = Course.objects.all()


    # Create a dictionary to store the analysis results for each course
    course_analysis = {}



    # Iterate over each course
    for course in courses:

        # Create lists to store the fetched data for the current course
        alumni_data = []
        current_job_data = []
        course_data = []



        # Populate the lists with the fetched data for the current course
        for alum in alumni.filter(course_id=course.course_id):
            alumni_data.append(alum)
            current_job = current_jobs.filter(alumni=alum).first()
            current_job_data.append(current_job)
            course_data.append(course)



        # Create a DataFrame from the fetched data for the current course
        data = {
            'Alumni': alumni_data,
            'Current Job': current_job_data,
            'Course': course_data
        }

        df = pd.DataFrame(data)



        # Perform the analysis for the current course
        df['Job Related to Course'] = df['Course'].apply(lambda x: x.field_type if x else None) == df['Current Job'].apply(lambda x: x.field_type if x else None)



        # Filtering out None values
        filtered_jobs = df.dropna(subset=['Job Related to Course'])



        # Counting related and non-related jobs
        related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == True].shape[0]
        non_related_count = filtered_jobs[filtered_jobs['Job Related to Course'] == False].shape[0]



        # Store the analysis results for the current course in the dictionary
        course_analysis[course.course_name] = {
            'Related_Jobs': related_count,
            'Non_related_Jobs': non_related_count
        }

    return course_analysis



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
    course_list = Course.objects.values_list('course_id', flat=True)  # Retrieve course IDs from the Course model

    total_students_list = []
    job_students_list = []
    percent_students_list = []

    for course_id in course_list:
        total_students = calculate_total_students(course_id)
        job_students = calculate_num_students_with_job(course_id)
        percent_students = (job_students / total_students) * 100 if total_students != 0 else 0

        total_students_list.append(total_students)
        job_students_list.append(job_students)
        percent_students_list.append(percent_students)

    plt.figure()

    plt.bar(course_list, job_students_list)
    plt.xlabel('Course')
    plt.ylabel('Number of Students with Job')
    plt.title('Percentage of Graduate Students with Job within 6 Months by Course')

    # Save the plot to a BytesIO object
    plot_buffer = io.BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    bar_plot_job_within_6_months = base64.b64encode(plot_buffer.read()).decode('utf-8')



    return bar_plot_job_within_6_months, percent_students_list, total_students_list, job_students_list
