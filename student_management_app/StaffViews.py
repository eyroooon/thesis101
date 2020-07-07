from django.shortcuts import render
from django.urls import reverse


def staff_home(request):
    return render(request, 'staff_templates/home_template.html')
