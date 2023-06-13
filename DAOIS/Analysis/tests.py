from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AlumniManagement.models import *
import random
import string


def generate_username():
	    """Generate a random username."""
	    letters = string.ascii_lowercase
	    random_string = ''.join(random.choice(letters) for _ in range(6))
	    return f'testuser_{random_string}'


class EmploymentPercentageTest(TestCase):

	

    def setUp(self):
        # Create alumni with jobs
        self.alumni_with_jobs = []
        for i in range(10):
            username = generate_username()
            password = 'testpassword'
            user = User.objects.create_user(username=username, password=password)

            course = Course.objects.create(
                course_id=f'C{i}',
                course_name=f'Bachelor of Science in Information Technology {i}',
                course_desc=f'A course in IT {i}',
                field_type='technology'
            )

            country = Country.objects.create(
                country_name=f'Test Country {i}'
            )

            province = Province.objects.create(
                province_name=f'Test Province {i}',
                country=country
            )

            city = City.objects.create(
                city_name=f'Test City {i}',
                province=province
            )

            barangay = Barangay.objects.create(
                barangay_name=f'Test Barangay {i}',
                city=city
            )

            alumni = Alumni_Demographic_Profile.objects.create(
                user=user,
                alumni_id=f'A{i}',
                fname=f'John {i}',
                lname=f'Doe {i}',
                mi='',
                suffix='',
                course_id=course,
                sex='male',
                religion='Christian',
                marital_status='Single',
                date_of_birth='1990-01-01',
                country_id=country.id,
                province_id=province.id,
                city_id=city.id,
                barangay_id=barangay.id
            )

            Current_Job.objects.create(
                current_job_id=f'J{i}',
                field_type='technology',
                job_title=f'Software Engineer {i}',
                salary=5000,
                start_date='2023-01-01',
                company_name=f'ABC Company {i}',
                alumni=alumni,
                country_id=country.id,
                province_id=province.id,
                city_id=city.id,
                barangay_id=barangay.id
            )

            self.alumni_with_jobs.append(alumni)


         # Create alumni without jobs
        self.alumni_without_jobs = []
        for i in range(6):
            username = generate_username()
            password = 'testpassword'
            user = User.objects.create_user(username=username, password=password)

            course = Course.objects.create(
                course_id=f'C{i + 10}',
                course_name=f'Bachelor of Science in Information Technology {i + 10}',
                course_desc=f'A course in IT {i + 10}',
                field_type='technology'
            )

            country = Country.objects.create(
                country_name=f'Test Country {i + 10}'
            )

            province = Province.objects.create(
                province_name=f'Test Province {i + 10}',
                country=country
            )

            city = City.objects.create(
                city_name=f'Test City {i + 10}',
                province=province
            )

            barangay = Barangay.objects.create(
                barangay_name=f'Test Barangay {i + 10}',
                city=city
            )

            alumni = Alumni_Demographic_Profile.objects.create(
                user=user,
                alumni_id=f'A{i + 10}',
                fname=f'Jane {i}',
                lname=f'Smith {i}',
                course_id=course,
                sex='female',
                religion='Christian',
                marital_status='Married',
                date_of_birth='1992-01-01',
                country_id=country.id,
                province_id=province.id,
                city_id=city.id,
                barangay_id=barangay.id
            )

            self.alumni_without_jobs.append(alumni)

    def test_calculate_employment_percentage(self):
        # Make a GET request to the URL associated with the view function
        response = self.client.get(reverse('Analysis:employment_percentage'))

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check that the JSON response contains the expected data
        data = response.json()
        self.assertEqual(data['labels'], ['Employed', 'Unemployed'])
        self.assertEqual(data['data'], [62.5, 37.5])
        if response.status_code:
        	msg = 'Thank you lord - Ok'
        else:
        	msg = 'Sakit sa Ulo'
        print('\nAnalysis for Employment Percentage: ', msg, response.status_code)


    def test_analyze_job_course_relation(self):
    	response = self.client.get(reverse('Analysis:analyze_job_course_relation'))

    	self.assertEqual(response.status_code, 200)

    	data = response.json()
    	self.assertEqual(data['labels'], ['Related to Course', 'Not Related to Course'])
    	self.assertEqual(data['data'], [62.5, 37.5])

    	if response.status_code:
    		msg = 'Swabe - Ok'
    	else: 
    		msg = 'Ewwww'
    	print('\nAnalysis for Job Relation: ', msg, response.status_code)

