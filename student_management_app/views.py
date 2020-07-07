from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here


def showLoginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>METHOD IS NOT ALLOWED</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse('adminHome'))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse('staffHome'))
            else:
                return HttpResponseRedirect(reverse('studentHome'))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def getUserDetails(request):
    if request.user != None:
        return HttpResponse("Email: " + request.user.email + " User Type: " + request.user.user_type)
    else:
        return HttpResponse("<h2>PLEASE LOG IN FIRST</h2>")


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')
