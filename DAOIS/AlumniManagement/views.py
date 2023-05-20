from django.shortcuts import render
from .models import *

import pandas as pd
import matplotlib.pyplot as plt

import io
import base64


def dashboard(request):
    alumni_id = "A10002"
    job_exists = Current_Job.objects.filter(alumni_id=alumni_id).exists()
    if job_exists:
    	print("has a job")
    else:
    	print("No job")

    total_alumni_count = Alumni_Demographic_Profile.objects.count()

    jobless_alumni_count = Alumni_Demographic_Profile.objects.filter(current_job__isnull=True).count()
    employed_alumni_count = total_alumni_count - jobless_alumni_count

    # Calculate the percentages
    jobless_percentage = (jobless_alumni_count / total_alumni_count) * 100
    employed_percentage = 100 - jobless_percentage

    # Create the pie chart
    labels = ['Jobless Alumni', 'Employed Alumni']
    sizes = [jobless_percentage, employed_percentage]
    explode = (0.1, 0)  # Explode the 'Jobless Alumni' slice
    colors = ['#ff9999', '#66b3ff']
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Alumni Job Status')

    # Convert the plot to an image for rendering in the template
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    context = {
        'jobless_percentage': jobless_percentage,
        'image_base64': image_base64,
    }

    return render(request, 'AlumniManagement/Dashboard.html', context)

# def dashboard(request):
# 	query = """
# 		SELECT a.alumni_id, a.fname, a.lname
# 	    FROM Alumni_Demographic_Profile AS a
# 	    LEFT JOIN Current_Job AS cj ON a.alumni_id = cj.alumni_id
# 	    WHERE cj.current_job_id IS NULL
#     """
#     df = pd.read_sql_query(query, connection)

    
    

#     # Count the number of alumni without jobs
#     jobless_count = len(df)

#     # Plot the count
#     plt.bar(["Alumni without Job"], [jobless_count])
#     plt.xlabel("Job Status")
#     plt.ylabel("Count")
#     plt.title("Number of Alumni without Jobs")

#     # Convert the plot to an image for rendering in the template
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
#     plt.close()



# 	alumni = pd.DataFrame(Alumni_Demographic_Profile.objects.all().values())

# 	return render(request, 'AlumniManagement/Dashboard.html', {
# 		'alumni': alumni.to_html(),
# 		'jobless_count': jobless_count,
#         'image_base64': image_base64,
# 		})