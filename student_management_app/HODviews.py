from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from student_management_app.models import *


def admin_home(request):
    return render(request, 'hod_templates/home_template.html')


def add_staff(request):
    return render(request, 'hod_templates/add_staff_template.html')


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staff.address = address
            user.save()
            messages.success(request, 'Sucessfully Added Staff')
            return HttpResponseRedirect('/add_staff')
        except:
            messages.error(request, 'Failed to Add Staff')
            return HttpResponseRedirect('/add_staff')


def add_course(request):
    return render(request, 'hod_templates/add_course_template.html')


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        course_name = request.POST.get('course_name')

        try:
            course = Courses(course_name=course_name)
            course.save()
            messages.success(request, 'Sucessfully Added Course')
            return HttpResponseRedirect('/add_course')
        except:
            messages.error(request, 'Failed to Add Course')
            return HttpResponseRedirect('/add_course')


def add_student(request):
    courses = Courses.objects.all()
    return render(request, 'hod_templates/add_student_template.html', {'courses': courses})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        course = request.POST.get('course')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        gender = request.POST.get('sex')

        if request.FILES['profile_pic']:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.student.address = address
            user.student.course_id = Courses.objects.get(id=course)
            user.student.gender = gender
            user.student.session_start_year = session_start
            user.student.session_end_year = session_end
            user.student.profile_pic = profile_pic_url
            user.save()
            messages.success(request, 'Sucessfully Added Student')
            return HttpResponseRedirect('/add_student')
        except:
            messages.error(request, 'Failed to Add Student')
            return HttpResponseRedirect('/add_student')


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_templates/add_subject_template.html', {'staffs': staffs, 'courses': courses})


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        subject_name = request.POST.get('subject_name')
        course = Courses.objects.get(id=request.POST.get('course'))
        staff = CustomUser.objects.get(id=request.POST.get('staff'))

        try:
            subject = Subject(subject_name=subject_name,
                              course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, 'Sucessfully Added Subject')
            return HttpResponseRedirect('/add_subject')
        except:
            messages.error(request, 'Failed to Add Subject')
            return HttpResponseRedirect('/add_subject')


def manage_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'hod_templates/manage_staff_template.html', {'staffs': staffs})


def manage_student(request):
    students = Student.objects.all()
    return render(request, 'hod_templates/manage_student_template.html', {'students': students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_templates/manage_course_template.html', {'courses': courses})


def manage_subject(request):
    subjects = Subject.objects.all()
    return render(request, 'hod_templates/manage_subject_template.html', {'subjects': subjects})


def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    return render(request, 'hod_templates/edit_staff_template.html', {'staff': staff, 'id': staff_id})


def edit_staff_save(request, staff_id):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.staff.address = address
            user.save()
            user.staff.save()
            messages.success(request, 'Sucessfully Updated Staff')
            return HttpResponseRedirect('/edit_staff/'+staff_id)
        except:
            messages.error(request, 'Failed to Edit Staff')
            return HttpResponseRedirect('/manage_staff' + staff_id)


def edit_student(request, student_id):
    courses = Courses.objects.all()
    student = Student.objects.get(admin=student_id)
    return render(request, 'hod_templates/edit_student_template.html', {'student': student, 'courses': courses, 'id': student_id})


def edit_student_save(request, student_id):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email')
        course = request.POST.get('course')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        gender = request.POST.get('sex')

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            course_id = Courses.objects.get(id=course)
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student = Student.objects.get(admin=student_id)
            student.address = address
            student.gender = gender
            student.session_start_year = session_start
            student.session_end_year = session_end
            student.course_id = course_id
            student.profile_pic = profile_pic_url
            student.save()
            messages.success(request, 'Sucessfully Updated Staff')
            return HttpResponseRedirect('/edit_student/'+student_id)
        except:
            messages.error(request, 'Failed to Edit Staff')
            return HttpResponseRedirect('/edit_student/' + student_id)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'hod_templates/edit_course_template.html', {'course': course, 'id': course_id})


def edit_course_save(request, course_id):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        course_name = request.POST.get('course_name')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, 'Sucessfully Edited Course')
            return HttpResponseRedirect('/edit_course/'+course_id)
        except:
            messages.error(request, 'Failed to Edit Course')
            return HttpResponseRedirect('/edit_course/'+course_id)


def edit_subject(request, subject_id):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    subject = Subject.objects.get(id=subject_id)
    return render(request, 'hod_templates/edit_subject_template.html', {'subject': subject, 'courses': courses, 'staffs': staffs, 'id': subject_id})


def edit_subject_save(request, subject_id):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        subject_name = request.POST.get('subject_name')
        course = Courses.objects.get(id=request.POST.get('course'))
        staff = CustomUser.objects.get(id=request.POST.get('staff'))

        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.course_id = course
            subject.staff_id = staff
            subject.save()
            messages.success(request, 'Sucessfully Edited Subject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)
        except:
            messages.error(request, 'Failed to Edit Subject')
            return HttpResponseRedirect('/edit_subject/'+subject_id)