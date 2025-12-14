
from django.shortcuts import render
from .models import SDGProject, SDG_CHOICES # Import both the model and the choices list

def project_list(request):
    # 1. Fetch all projects from the database
    projects = SDGProject.objects.all().order_by('-created_at') 

    # 2. Package the data to send to the template
    context = {
        'projects': projects,
        'sdg_choices': dict(SDG_CHOICES) # Convert the choices list to a dictionary for easier lookup
    }

    # 3. Render the template
    return render(request, 'sdg_platform/project_list.html', context)