from django.shortcuts import render
from django.urls import reverse


def student_home(request):
    return render(request, 'student_templates/home_template.html')
