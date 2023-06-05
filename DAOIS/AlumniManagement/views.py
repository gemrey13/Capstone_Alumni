from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *


def your_view(request):
    countries = Country.objects.all()
    provinces = Province.objects.all()
    cities = City.objects.all()
    barangays = Barangay.objects.all()

    context = {
        'countries': countries,
        'provinces': provinces,
        'cities': cities,
        'barangays': barangays,
    }

    return render(request, 'power.html', context)

def get_barangays(request):
    city_id = request.GET.get('city_id')
    barangays = Barangay.objects.filter(city_id=city_id).values('id', 'barangay_name')

    return JsonResponse({'barangays': list(barangays)})

def get_provinces(request):
    country_id = request.GET.get('country_id')
    provinces = Province.objects.filter(country_id=country_id).values('id', 'province_name')

    return JsonResponse({'provinces': list(provinces)})

def get_cities(request):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id).values('id', 'city_name')

    return JsonResponse({'cities': list(cities)})



def alumni_search(request):
    query = request.GET.get('query', '')
    profiles = Alumni_Demographic_Profile.objects.filter(
        fname__icontains=query
    )
    html = render_to_string('AlumniManagement/components/alumni_search.html', {'profiles': profiles})
    return JsonResponse({'html': html})


@login_required(login_url='Authentication:login')
def dashboard(request):
    course_analysis = course_related_job_analysis()
    context = {
        'course_analysis': course_analysis,
    }
    return render(request, 'AlumniManagement/Dashboard.html', context)


@login_required(login_url='Authentication:login')
def alumni(request):
    profiles = Alumni_Demographic_Profile.objects.all()
    context = {
        'profiles': profiles,
    }
    return render(request, "AlumniManagement/alumni.html", context)
    

@login_required(login_url='Authentication:login')
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


