from django.urls import path
from . import utils

urlpatterns = [
    path('employment-percentage/', utils.calculate_employment_percentage, name='employment_percentage'),
    path('job-course-relation/', utils.analyze_job_course_relation, name='analyze_job_course_relation'),
    path('alumni-with-jobs-per-course/', utils.analyze_alumni_with_jobs_per_course, name='analyze_alumni_with_jobs_per_course'),
    path('alumni-with-jobs-within-six-months/', utils.analyze_alumni_with_jobs_within_six_months, name="analyze_alumni_with_jobs_within_six_months"),
    path('job-field-distribution/', utils.analyze_job_field_distribution, name='analyze_job_field_distribution')
]
