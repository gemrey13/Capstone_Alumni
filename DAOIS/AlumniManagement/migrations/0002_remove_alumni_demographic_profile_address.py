# Generated by Django 4.2.1 on 2023-05-31 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AlumniManagement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumni_demographic_profile',
            name='address',
        ),
    ]