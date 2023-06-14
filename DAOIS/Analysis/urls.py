from django.urls import path
from . import utils

app_name = "Analysis"

urlpatterns = [
    path('employment-percentage/', utils.calculate_employment_percentage, name='employment_percentage'),
    path('job-course-relation/', utils.analyze_job_course_relation, name='analyze_job_course_relation'),
    path('alumni-with-jobs-per-course/', utils.analyze_alumni_with_jobs_per_course, name='analyze_alumni_with_jobs_per_course'),
    path('alumni-with-jobs-within-six-months/', utils.analyze_alumni_with_jobs_within_six_months, name="analyze_alumni_with_jobs_within_six_months"),
    path('job-field-distribution/', utils.analyze_job_field_distribution, name='analyze_job_field_distribution'),
    path('salary-by-field/', utils.analyze_salary_by_field, name='analyze_salary_by_field'),
    path('employment-gap/', utils.analyze_employment_gap, name='analyze_employment_gap'),
    path('promotion-rates/', utils.analyze_promotion_rates, name='analyze_promotion_rates'),
    path('alumi-per-course/', utils.alumi_per_course, name='alumi_per_course'),
]
