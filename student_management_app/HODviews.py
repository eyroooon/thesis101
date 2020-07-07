from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import *
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
            return HttpResponseRedirect(reverse('addStaff'))
        except:
            messages.error(request, 'Failed to Add Staff')
            return HttpResponseRedirect(reverse('addStaff'))


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
            return HttpResponseRedirect(reverse('addCourse'))
        except:
            messages.error(request, 'Failed to Add Course')
            return HttpResponseRedirect(reverse('addCourse'))


def add_student(request):
    form = AddStudentForm()
    return render(request, 'hod_templates/add_student_template.html', {'form': form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']
            session_start = form.cleaned_data['session_start']
            session_end = form.cleaned_data['session_end']
            gender = form.cleaned_data['sex']

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
                return HttpResponseRedirect(reverse('addStudent'))
            except:
                messages.error(request, 'Failed to Add Student')
                return HttpResponseRedirect(reverse('addStudent'))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'hod_templates/add_student_template.html', {'form': form})


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
            return HttpResponseRedirect(reverse('addSubject'))
        except:
            messages.error(request, 'Failed to Add Subject')
            return HttpResponseRedirect(reverse('addSubject'))


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
            return HttpResponseRedirect(reverse('manageStaff', kwargs={'staff_id': staff_id}))
        except:
            messages.error(request, 'Failed to Edit Staff')
            return HttpResponseRedirect(reverse('manageStaff', kwargs={'staff_id': staff_id}))


def edit_student(request, student_id):
    courses = Courses.objects.all()
    student = Student.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_start'].initial = student.session_start_year
    form.fields['session_end'].initial = student.session_end_year
    return render(request, 'hod_templates/edit_student_template.html', {'form': form, 'student': student})


def edit_student_save(request, student_id):
    if request.method != 'POST':
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            course = form.cleaned_data['course']
            session_start = form.cleaned_data['session_start']
            session_end = form.cleaned_data['session_end']
            gender = form.cleaned_data['sex']

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
                return HttpResponseRedirect(reverse('editStudent', kwargs={'student_id': student_id}))
            except:
                messages.error(request, 'Failed to Edit Staff')
                return HttpResponseRedirect(reverse('editStudent', kwargs={'student_id': student_id}))

        else:
            form = EditStudentForm(request.POST, request.FILES)
            student = Student.objects.get(admin=student_id)
            return render(request, 'hod_templates/edit_student_template.html', {'form': form, 'student': student})


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
            return HttpResponseRedirect(reverse('editCourse', kwargs={'course_id': course_id}))

        except:
            messages.error(request, 'Failed to Edit Course')
            return HttpResponseRedirect(reverse('editCourse', kwargs={'course_id': course_id}))


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
            return HttpResponseRedirect(reverse('editSubject', kwargs={'subject_id': subject_id}))

        except:
            messages.error(request, 'Failed to Edit Subject')
            return HttpResponseRedirect(reverse('editSubject', kwargs={'subject_id': subject_id}))
