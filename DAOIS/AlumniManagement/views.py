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
    jobcountry_id = request.GET.get('jobcountry_id')
    provinces = Province.objects.filter(country_id=country_id).values('id', 'province_name')
    jobprovinces = Province.objects.filter(country_id=jobcountry_id).values('id', 'province_name')

    return JsonResponse({'provinces': list(provinces), 'jobprovinces': list(jobprovinces)})

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
    countries = Country.objects.all()
    courses = Course.objects.all()
    field_choices = FIELD_CHOICES
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        print(fname)
        lname = request.POST.get('lname')
        mi = request.POST.get('mi')
        suffix = request.POST.get('suffix')
        course_id = request.POST.get('country')
        alumni_id = request.POST.get('alumni_id')
        marital_status = request.POST.get('marital_status')
        date_of_birth = request.POST.get('date_of_birth')
        religion = request.POST.get('religion')
        sex = request.POST.get('sex')
        country = request.POST.get('country')
        province = request.POST.get('province')
        city = request.POST.get('city')
        barangay = request.POST.get('barangay')
        #-----------------------------------------------
        current_job_id = request.POST.get('current_job_id')
        field_type = request.POST.get('field_type')
        job_title = request.POST.get('job_title')
        print(job_title)
        salary = request.POST.get('salary')
        start_date = request.POST.get('start_date')
        company_name = request.POST.get('company_name')
        country = request.POST.get('job_country')
        province = request.POST.get('job_province')
        city = request.POST.get('job_city')
        barangay = request.POST.get('job_barangay')


        new_alumni = Alumni_Demographic_Profile(alumni_id=alumni_id, fname=fname, lname=lname, mi=mi, suffix=suffix, course_id=course_id, sex=sex, religion=religion, marital_status=marital_status, date_of_birth=date_of_birth, country=country, province=province, city=city, barangay=barangay)
        new_alumni.save()

        new_job = Current_Job(alumni=new_alumni, current_job_id=current_job_id, field_type=field_type, job_title=job_title, salary=salary, start_date=start_date, company_name=company_name, country=country, province=province, city=city, barangay=barangay)
        new_job.save()

    context = {
        'profiles': profiles,
        'countries': countries,
        'courses': courses,
        'field_choices': field_choices,
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


