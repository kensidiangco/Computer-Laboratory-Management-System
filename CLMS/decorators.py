from django.http import HttpResponseRedirect
from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
        
        
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'staff':
            return HttpResponseRedirect(reverse('userPage'))
            
        if group == 'IT_Dept':
            return HttpResponseRedirect(reverse('ITDeptDashboard'))
            
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper

def ITDept_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'staff':
            return HttpResponseRedirect(reverse('userPage'))

        if group == 'admin':
            return HttpResponseRedirect(reverse('adminDashboard'))
            
        elif group == 'IT_Dept':
            return view_func(request, *args, **kwargs)
    return wrapper