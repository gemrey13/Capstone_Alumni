from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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



@login_required(login_url='Authentication:login')
def dashboard(request):
    context = {
    }
    return render(request, 'AlumniManagement/Dashboard.html', context)


@login_required(login_url='Authentication:login')
def alumni(request):
    profiles = Alumni_Demographic_Profile.objects.order_by('sex')
    alumni_count = Alumni_Demographic_Profile.objects.all().count()
    countries = Country.objects.all()
    courses = Course.objects.all()
    
    if request.method == "POST":

        try:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            mi = request.POST.get('mi')
            suffix = request.POST.get('suffix')
            course_id = request.POST.get('course')
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
            graduate_id = request.POST.get('graduate_id')
            graduation_date = request.POST.get('graduation_date')
            honor = request.POST.get('honor')
            #-----------------------------------------------
            current_job_id = request.POST.get('current_job_id')
            field_type = request.POST.get('field_type')
            job_title = request.POST.get('job_title')
            salary = request.POST.get('salary')
            start_date = request.POST.get('start_date')
            company_name = request.POST.get('company_name')
            job_country = request.POST.get('job_country')
            job_province = request.POST.get('job_province')
            job_city = request.POST.get('job_city')
            job_barangay = request.POST.get('job_barangay')

            #----------------------------------------------------
            if fname and lname and course_id and date_of_birth and sex and alumni_id:
                if current_job_id and field_type and job_title and start_date and salary and company_name and job_country and job_city and job_province and job_barangay:
                    course = Course.objects.get(course_id=course_id)
                    country = Country.objects.get(id=country)
                    province = Province.objects.get(id=province)
                    city = City.objects.get(id=city)
                    barangay = Barangay.objects.get(id=barangay)
                    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                    new_alumni = Alumni_Demographic_Profile(alumni_id=alumni_id, fname=fname, lname=lname, mi=mi, suffix=suffix, 
                                                            course_id=course, sex=sex, religion=religion, 
                                                            marital_status=marital_status, date_of_birth=date_of_birth, 
                                                            country=country, province=province, city=city, barangay=barangay)
                    new_alumni.save()
                    
                    new_alumni_graduate = Graduate(graduate_id=graduate_id, alumni=new_alumni, graduation_date=graduation_date, honor=honor)
                    new_alumni_graduate.save()

                    job_country = Country.objects.get(id=job_country)
                    job_province = Province.objects.get(id=job_province)
                    job_city = City.objects.get(id=job_city)
                    job_barangay = Barangay.objects.get(id=job_barangay)
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    new_job = Current_Job(alumni=new_alumni, current_job_id=current_job_id, field_type=field_type, job_title=job_title, 
                                        salary=salary, start_date=start_date, company_name=company_name, 
                                        country=job_country, province=job_province, city=job_city, barangay=job_barangay)
                    new_job.save()
                    messages.success(request, 'Sucess Add alumni and his/her current job.')
                else:
                    if not country or not province or not city or not barangay:
                        raise ValueError('Please Provide a Address.')
                    else:
                        course = Course.objects.get(course_id=course_id)
                        country = Country.objects.get(id=country)
                        province = Province.objects.get(id=province)
                        city = City.objects.get(id=city)
                        barangay = Barangay.objects.get(id=barangay)
                        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                        new_alumni = Alumni_Demographic_Profile(alumni_id=alumni_id, fname=fname, lname=lname, mi=mi, suffix=suffix, 
                                                                course_id=course, sex=sex, religion=religion, 
                                                                marital_status=marital_status, date_of_birth=date_of_birth, 
                                                                country=country, province=province, city=city, barangay=barangay)
                        new_alumni.save()
                        
                        new_alumni_graduate = Graduate(graduate_id=graduate_id, alumni=new_alumni, graduation_date=graduation_date, honor=honor)
                        new_alumni_graduate.save()

                        messages.success(request,'Sucess Add alumni.')
            elif not fname or not lname or not course_id or not date_of_birth or not religion or not marital_status or not sex:
                raise ValueError('Please Provide a Valid Alumni Input.')
                
            
        except ValueError as e:
            messages.error(request, str(e))
            print(e)

        except Exception as e:
            messages.error(request, 'An error occured: ', str(e))
            print(e)

        return redirect('AlumniManagement:alumni')

    paginator = Paginator(profiles, 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        # Redirect or handle the invalid page number case
        page_obj = paginator.get_page(1)  # Redirect to the first page

    total_pages = paginator.num_pages
    max_page_buttons = 5

    # Calculate the range of page numbers to show
    middle_button = max_page_buttons // 2

    if total_pages <= max_page_buttons:
        page_range = range(1, total_pages + 1)
    elif page_obj.number <= middle_button:
        page_range = range(1, max_page_buttons + 1)
    elif page_obj.number >= total_pages - middle_button:
        page_range = range(total_pages - max_page_buttons + 1, total_pages + 1)
    else:
        page_range = range(page_obj.number - middle_button, page_obj.number + middle_button + 1)

    context = {
        'countries': countries,
        'courses': courses,
        'field_choices': FIELD_CHOICES,
        'sex_choices': SEX_CHOICES,
        'profiles': page_obj.object_list,
        'page':page_obj,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_range': page_range,
        'alumni_count': alumni_count,
    }
    return render(request, "AlumniManagement/alumni.html", context)


def alumni_profile(request, alumni_id):
    alumni = Alumni_Demographic_Profile.objects.get(alumni_id=alumni_id)
    graduate = Graduate.objects.get(alumni=alumni)
    current_jobs = Current_Job.objects.filter(alumni__alumni_id=alumni_id)
    prev_jobs = Previous_Job.objects.filter(alumni__alumni_id=alumni_id)
    countries = Country.objects.all()
    courses = Course.objects.all()

    alumni_country = alumni.country
    alumni_province = alumni.province
    alumni_city = alumni.city
    alumni_barangay = alumni.barangay

    alumni_course_id = str(alumni.course_id)

    context = {
        'alumni':alumni,
        'graduate': graduate,
        'countries': countries,
        'current_jobs': current_jobs,
        'prev_jobs': prev_jobs,
        'courses': courses,
        'alumni_course_id': alumni_course_id,
        'field_choices': FIELD_CHOICES,
        'sex_choices': SEX_CHOICES,
        'alumni_country': alumni_country,
        'alumni_province': alumni_province,
        'alumni_city': alumni_city,
        'alumni_barangay': alumni_barangay,
    }

    return render(request, 'AlumniManagement/alumni_profile.html', context)
    

def sample2(request):
    return render(request, 'AlumniManagement/sample2.html')