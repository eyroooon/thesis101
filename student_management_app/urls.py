from django.urls import path
from . import views, HODviews, StudentViews, StaffViews

urlpatterns = [
    path('', views.showLoginPage, name='login'),
    path('do_login', views.doLogin, name='doLogin'),
    path('logout', views.logoutUser, name='logoutUser'),
    path('get_user_details', views.getUserDetails, name='getUserDetails'),
    path('admin_home', HODviews.admin_home, name='adminHome'),
    path('add_staff', HODviews.add_staff, name='addStaff'),
    path('add_staff_save', HODviews.add_staff_save, name='addStaffSave'),
    path('add_course', HODviews.add_course, name='addCourse'),
    path('add_course_save', HODviews.add_course_save, name='addCourseSave'),
    path('add_student', HODviews.add_student, name='addStudent'),
    path('add_student_save', HODviews.add_student_save, name='addStudentSave'),
    path('add_subject', HODviews.add_subject, name='addSubject'),
    path('add_subject_save', HODviews.add_subject_save, name='addSubjectSave'),
    path('manage_staff', HODviews.manage_staff, name='manageStaff'),
    path('manage_student', HODviews.manage_student, name='manageStudent'),
    path('manage_course', HODviews.manage_course, name='manageCourse'),
    path('manage_subject', HODviews.manage_subject, name='manageSubject'),
    path('edit_staff/<str:staff_id>/', HODviews.edit_staff, name='editStaff'),
    path('edit_staff_save/<str:staff_id>/',
         HODviews.edit_staff_save, name='editStaffSave'),
    path('edit_student/<str:student_id>/',
         HODviews.edit_student, name='editStudent'),
    path('edit_student_save/<str:student_id>/',
         HODviews.edit_student_save, name='editStudentSave'),
    path('edit_course/<str:course_id>/',
         HODviews.edit_course, name='editCourse'),
    path('edit_course_save/<str:course_id>/',
         HODviews.edit_course_save, name='editCourseSave'),
    path('edit_subject/<str:subject_id>/',
         HODviews.edit_subject, name='editSubject'),
    path('edit_subject_save/<str:subject_id>/',
         HODviews.edit_subject_save, name='editSubjectSave'),

    # Staff Path
    path('staff_home', StaffViews.staff_home, name='staffHome'),

    # Student Path
    path('student_home', StudentViews.student_home, name='studentHome'),


]
