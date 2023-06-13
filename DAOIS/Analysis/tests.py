from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AlumniManagement.models import *


class EmploymentPercentageTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')

        # Create a course
        course = Course.objects.create(
            course_id='C10001',
            course_name='Bachelor of Science in Information Technology',
            course_desc='A course in IT',
            field_type='technology'
        )

        country = Country.objects.create(
            country_name='Test Country'
        )

        # Create a province
        province = Province.objects.create(
            province_name='Test Province',
            country=country
        )

        city = City.objects.create(
            city_name='Test City',
            province=province
        )
        barangay = Barangay.objects.create(
            barangay_name='Test Barangay',
            city=city
        )
        # Create an alumni with a current job
        self.alumni_with_job = Alumni_Demographic_Profile.objects.create(
            user=self.user,
            alumni_id='A10001',
            fname='John',
            lname='Doe',
            mi='',
            suffix='',
            course_id=course,
            sex='male',
            religion='Christian',
            marital_status='Single',
            date_of_birth='1990-01-01',
            country_id=country.id,
            province_id=province.id,  # Assign the province instance
            city_id=city.id,
            barangay_id=barangay.id
        )

        Current_Job.objects.create(
            current_job_id='J10001',
            field_type='technology',
            job_title='Software Engineer',
            salary=5000,
            start_date='2023-01-01',
            company_name='ABC Company',
            alumni=self.alumni_with_job,
            country_id=1,
            province_id=1,
            city_id=1,
            barangay_id=1
        )

        # Create an alumni without a current job
        self.alumni_without_job = Alumni_Demographic_Profile.objects.create(
            user=self.user2,
            alumni_id='A10002',
            fname='Jane',
            lname='Smith',
            course_id=course,
            sex='female',
            religion='Christian',
            marital_status='Married',
            date_of_birth='1992-01-01',
            country_id=country.id,
            province_id=province.id,  # Assign the province instance
            city_id=city.id,
            barangay_id=barangay.id
        )

    def test_calculate_employment_percentage(self):
        # Make a GET request to the URL associated with the view function
        response = self.client.get(reverse('Analysis:employment_percentage'))

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check that the JSON response contains the expected data
        data = response.json()
        self.assertEqual(data['labels'], ['Employed', 'Unemployed'])
        self.assertEqual(data['data'], [50.0, 50.0])
