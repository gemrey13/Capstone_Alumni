import pandas as pd
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from AlumniManagement.models import *


# Analyze the employment of all alumni
# response is labels and data
def calculate_employment_percentage(request):
    alumni_count = Alumni_Demographic_Profile.objects.count()
    employed_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=False).count()

    employment_percentage = round((employed_count / alumni_count) * 100, 2)

    data = {
        'labels': ['Employed', 'Unemployed'],
        'data': [employment_percentage, 100 - employment_percentage]
    }

    return JsonResponse(data)


# Get the alumni and current job
# Analyze the relation of job and course
def analyze_job_course_relation(request):
    alumni_count = Alumni_Demographic_Profile.objects.count()
    related_job_count = Current_Job.objects.filter(alumni__course_id=models.F('alumni__course_id')).count()

    job_course_percentage = round((related_job_count / alumni_count) * 100, 2)

    data = {
        'labels': ['Related to Course', 'Not Related to Course'],
        'data': [job_course_percentage, 100 - job_course_percentage]
    }

    return JsonResponse(data)


# get the alumni with job by course
def analyze_alumni_with_jobs_per_course(request):
    courses = Course.objects.all()
    data = []

    for course in courses:
        alumni_count = Alumni_Demographic_Profile.objects.filter(course_id=course).count()
        employed_count = Current_Job.objects.filter(alumni__course_id=course).count()

        if alumni_count > 0:
            employment_percentage = round((employed_count / alumni_count) * 100, 2)
        else:
            employment_percentage = 0

        course_data = {
            'course_name': course.course_name,
            'employment_percentage': employment_percentage
        }
        data.append(course_data)

    return JsonResponse(data, safe=False)


# alumni and its course and job within six months
def analyze_alumni_with_jobs_within_six_months(request):
    courses = Course.objects.all()
    data = []

    for course in courses:
        alumni_count = Alumni_Demographic_Profile.objects.filter(course_id=course).count()
        graduates = Graduate.objects.filter(alumni__course_id=course)

        employed_count = 0
        for graduate in graduates:
            graduation_date = graduate.graduation_date
            six_months_after_graduation = graduation_date + timedelta(days=180)
            has_job_within_six_months = Current_Job.objects.filter(alumni=graduate.alumni, start_date__lte=six_months_after_graduation).exists()

            if has_job_within_six_months:
                employed_count += 1

        if alumni_count > 0:
            employment_percentage = round((employed_count / alumni_count) * 100, 2)
        else:
            employment_percentage = 0

        course_data = {
            'course_name': course.course_name,
            'employment_percentage': employment_percentage
        }
        data.append(course_data)

    return JsonResponse(data, safe=False)


# Get the job by field type
def analyze_job_field_distribution(request):
    field_distribution = Current_Job.objects.values('field_type').annotate(job_count=Count('field_type'))

    data = []
    total_jobs = 0

    for item in field_distribution:
        field_type = item['field_type']
        job_count = item['job_count']
        total_jobs += job_count

        field_data = {
            'field_type': field_type,
            'job_count': job_count
        }
        data.append(field_data)

    for item in data:
        item['percentage'] = round((item['job_count'] / total_jobs) * 100, 2)

    return JsonResponse(data, safe=False)

# Average salary by field
def analyze_salary_by_field(request):
    current_jobs = Current_Job.objects.all()

    current_jobs_data = []
    for job in current_jobs:
        current_jobs_data.append({
            'field_type': job.field_type,
            'salary': job.salary,
        })

    current_jobs_df = pd.DataFrame(current_jobs_data)

    average_salary_by_field = current_jobs_df.groupby('field_type')['salary'].mean().reset_index()
    average_salary_by_field['salary'] = average_salary_by_field['salary'].round(2)

    analysis_result = average_salary_by_field.to_dict(orient='records')
    data = {
        'analysis': analysis_result
    }

    return JsonResponse(data)


# Analyze End date of previous job and start date of current job to  get the average employment gap
def analyze_employment_gap(request):
    alumni = Alumni_Demographic_Profile.objects.all()
    employment_gaps = []

    for alumnus in alumni:
        previous_jobs = Previous_Job.objects.filter(alumni=alumnus).order_by('-end_date')
        current_job = Current_Job.objects.filter(alumni=alumnus).first()

        if previous_jobs and current_job:
            latest_end_date = previous_jobs[0].end_date
            gap = (current_job.start_date - latest_end_date).days
            employment_gaps.append({
                'alumni_id': alumnus.alumni_id,
                'employment_gap': gap
            })

    if employment_gaps:
        employment_gaps_df = pd.DataFrame(employment_gaps)
        avg_employment_gap = employment_gaps_df['employment_gap'].mean()
    else:
        avg_employment_gap = 0

    response_data = {
        'average_employment_gap': avg_employment_gap
    }

    return JsonResponse(response_data)


# The calculation of the promotion rate is based on the salary comparison between consecutive jobs. If the salary of a 
# job is higher than the salary of the previous job, it is considered a promotion. However, 
# if there are no instances where the salary increases from one job to the next, the promotion rate will be zero.
def analyze_promotion_rates(request):
    alumni = Alumni_Demographic_Profile.objects.all()
    promotion_rates = []

    for alumnus in alumni:
        current_jobs = Current_Job.objects.filter(alumni=alumnus).order_by('start_date')
        previous_jobs = Previous_Job.objects.filter(alumni=alumnus).order_by('end_date')
        
        job_count = len(current_jobs) + len(previous_jobs)
        
        if job_count > 1:
            promotions = 0

            # Check promotions in current jobs
            for i in range(1, len(current_jobs)):
                if current_jobs[i].salary > current_jobs[i-1].salary:
                    promotions += 1

            # Check promotions from previous jobs to current jobs
            if previous_jobs:
                if previous_jobs.last().salary < current_jobs.first().salary:
                    promotions += 1

            promotion_rate = promotions / (job_count - 1)  # Exclude the first job

            promotion_rates.append({
                'alumni_id': alumnus.alumni_id,
                'promotion_rate': promotion_rate
            })

    if promotion_rates:
        promotion_rates_df = pd.DataFrame(promotion_rates)
        avg_promotion_rate = promotion_rates_df['promotion_rate'].mean()
        avg_promotion_rate = round(avg_promotion_rate, 2)
    else:
        avg_promotion_rate = 0

    response_data = {
        'average_promotion_rate': avg_promotion_rate
    }

    return JsonResponse(response_data)
