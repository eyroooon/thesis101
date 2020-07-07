from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginCheckMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        if user.is_authenticated:
            if user.user_type == '1':
                if modulename == 'student_management_app.HODviews':
                    pass
                elif modulename == 'student_management_app.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('adminHome'))

            elif user.user_type == '2':
                if modulename == 'student_management_app.StaffViews':
                    pass
                elif modulename == 'student_management_app.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('staffHome'))

            elif user.user_type == '3':
                if modulename == 'student_management_app.StudentViews':
                    pass
                elif modulename == 'student_management_app.views':
                    pass
                else:
                    return HttpResponseRedirect(reverse('studentHome'))

            else:
                return HttpResponseRedirect(reverse('login'))
        else:
            if request.path == reverse('login') or request.path == reverse('doLogin'):
                pass
            else:
                return HttpResponseRedirect(reverse('login'))
