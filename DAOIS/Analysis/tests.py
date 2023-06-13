from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from AlumniManagement.models import *

from .utils import analyze_employment_gap
from datetime import datetime, timedelta
import uuid
import json
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

            start_date = datetime(2023, 1, 1) + timedelta(days=i)
            Current_Job.objects.create(
                current_job_id=f'CJ{i}',
                field_type='technology',
                job_title=f'Current Job {i}',
                salary=5000,
                start_date=start_date,
                company_name=f'Current Company {i}',
                alumni=alumni,
                country_id=country.id,
                province_id=province.id,
                city_id=city.id,
                barangay_id=barangay.id
            )

            for j in range(i):
                previous_job_id = f'J{i}_{uuid.uuid4().hex}'
                start_date = datetime(2022, 1, 1) + timedelta(days=j)
                end_date = datetime(2022, 12, 31) - timedelta(days=i-j)
                Previous_Job.objects.create(
                    previous_job_id=previous_job_id,
                    field_type='technology',
                    job_title=f'Previous Job {j}',
                    salary=4000,
                    start_date=start_date,
                    end_date=end_date,
                    company_name=f'Previous Company {j}',
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
        print('\nAnalysis for Employment Percentage: ', msg, response.status_code, data)


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
    	print('\nAnalysis for Job Relation: ', msg, response.status_code, data)


    def test_analyze_employment_gap(self):
        factory = RequestFactory()
        request = factory.get(reverse('Analysis:analyze_employment_gap'))
        response = analyze_employment_gap(request)

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check the expected average employment gap value
        # expected_avg_employment_gap = 7  # Assuming 1-year gap
        # data = json.loads(response.content)
        # self.assertEqual(data['average_employment_gap'], expected_avg_employment_gap)
        data = json.loads(response.content)

        # Check that the response has the expected status code
        self.assertEqual(response.status_code, 200)

        # Check that the response data contains the expected keys
        self.assertIn('average_employment_gap', data)

        # Check the type and value range of the average employment gap
        self.assertIsInstance(data['average_employment_gap'], float)
        self.assertGreaterEqual(data['average_employment_gap'], 0)


        if response.status_code:
            msg = 'Naysu - Ok'
        else:
            msg = 'LOL'
        print('\nAnalysis for Employemnt Gap: ', msg, response.status_code, data)