from ast import Name
from django.http import HttpResponseRedirect
from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('adminDashboard'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
        
        
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'prof':
            return HttpResponseRedirect(reverse('profDashboard'))
            
        if group == 'IT_Dept':
            return HttpResponseRedirect(reverse('ITDeptDashboard'))

        if group == 'dean':
            return HttpResponseRedirect(reverse('deanDashboard'))
            
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper

def ITDept_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'prof':
            return HttpResponseRedirect(reverse('profDashboard'))

        if group == 'admin':
            return HttpResponseRedirect(reverse('adminDashboard'))
        
        if group == 'dean':
            return HttpResponseRedirect(reverse('deanDashboard'))
            
        elif group == 'IT_Dept':
            return view_func(request, *args, **kwargs)
    return wrapper

def prof_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'IT_Dept':
            return HttpResponseRedirect(reverse('ITDeptDashboard'))

        if group == 'admin':
            return HttpResponseRedirect(reverse('adminDashboard'))
        
        if group == 'dean':
            return HttpResponseRedirect(reverse('deanDashboard'))
            
        elif group == 'prof':
            return view_func(request, *args, **kwargs)
    return wrapper

def dean_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'IT_Dept':
            return HttpResponseRedirect(reverse('ITDeptDashboard'))

        if group == 'admin':
            return HttpResponseRedirect(reverse('adminDashboard'))
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('profDashboard'))
            
        elif group == 'dean':
            return view_func(request, *args, **kwargs)
    return wrapper

def admin_pending_sched_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('Prof_Pending_Schedule'))
            
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def admin_approved_sched_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('Prof_Approved_Schedule'))
            
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def admin_rejected_sched_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('Prof_Rejected_Schedule'))
            
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def admin_ongoing_sched_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('Prof_Ongoing_Schedule'))
            
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def admin_done_sched_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'prof':
            return HttpResponseRedirect(reverse('Prof_Done_Schedule'))
            
        else:
            return view_func(request, *args, **kwargs)
    return wrapper