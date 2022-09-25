from contextlib import redirect_stderr
from typing import ContextManager
from urllib.robotparser import RequestRate
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from ...decorators import dean_only, unauthenticated_user, admin_only, ITDept_only, prof_only
from django.contrib.auth.models import Group
from .models import Theme, Profile
from ..transaction.models import Sched_Request
from django.urls import reverse_lazy
from django.core.paginator import Paginator

@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def profRegisterPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            user.save()
            group = Group.objects.get(name='prof')
            user.groups.add(group)
            
            messages.success(request, 'Account successfully created for ' + username)
            return HttpResponseRedirect(reverse('loginPage'))
            
        else:
            messages.error(request, form.errors)
            
    return render(request, './account/prof/profRegister.html', { 'registerForm': form })
    
@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def deanRegisterPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            user.save()
            group = Group.objects.get(name='dean')
            user.groups.add(group)
            
            messages.success(request, 'Account successfully created for ' + username)
            return HttpResponseRedirect(reverse('loginPage'))
            
        else:
            messages.error(request, form.errors)
            
    return render(request, './account/dean/deanRegister.html', { 'registerForm': form })
    
@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def ITDeptAccountRegister(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            user.save()
            group = Group.objects.get(name='IT_Dept')
            user.groups.add(group)
            
            messages.success(request, 'Account successfully created for ' + username)
            return HttpResponseRedirect(reverse('loginPage'))
            
        else:
            messages.error(request, form.errors)
            
    return render(request, './account/itdept/ITDeptAccountRegister.html', { 'registerForm': form })

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.error(request, 'Check your password!')
            
    return render(request, './account/login.html')

def profile(request):
    return render(request, './account/profile.html')

def index(request):

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color
    }

    return render(request, './index.html', context)

def theme(request):
    color = request.GET.get('color')

    if color == 'dark':
        if Theme.objects.filter(user=request.user.username).exists():
            user_theme = Theme.objects.get(user=request.user.username)
            user_theme.user = request.user.username
            user_theme.color = 'dark'
            user_theme.save()
        else:
            user2 = Theme(user=request.user.username, color='dark')
            user2.save()

    elif color == 'light':
        if Theme.objects.filter(user=request.user.username).exists():
            user_theme = Theme.objects.get(user=request.user.username)
            user_theme.user = request.user.username
            user_theme.color = 'light'
            user_theme.save()
        else:
            user2 = Theme(user=request.user.username, color='light')
            user2.save()

    return HttpResponseRedirect(reverse('adminDashboard'))

@login_required(login_url=reverse_lazy("loginPage"))
def formPage(request):
    return render(request, './account/forms.html')
    
@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def adminDashboard(request):
    pending = Sched_Request.objects.filter(status="Pending")
    approved = Sched_Request.objects.filter(status="Approved")
    rejected = Sched_Request.objects.filter(status="Rejected")
    onGoing = Sched_Request.objects.filter(status="On going")
    done = Sched_Request.objects.filter(status="Done")

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'onGoing': onGoing,
        'done': done
    }
    return render(request, './account/admin/dashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
@dean_only
def deanDashboard(request):
    pending = Sched_Request.objects.filter(status="Pending")
    approved = Sched_Request.objects.filter(status="Approved")
    rejected = Sched_Request.objects.filter(status="Rejected")
    onGoing = Sched_Request.objects.filter(status="On going")
    done = Sched_Request.objects.filter(status="Done")

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'onGoing': onGoing,
        'done': done
    }
    return render(request, './account/dean/deanDashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
@ITDept_only
def ITDeptDashboard(request):
    pending = Sched_Request.objects.filter(status="Pending")
    approved = Sched_Request.objects.filter(status="Approved")
    rejected = Sched_Request.objects.filter(status="Rejected")
    onGoing = Sched_Request.objects.filter(status="On going")
    done = Sched_Request.objects.filter(status="Done")

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'onGoing': onGoing,
        'done': done
    }
    return render(request, './account/itdept/dashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url=reverse_lazy("loginPage"))
@prof_only
def profDashboard(request):
    sched = Sched_Request.objects.filter(requester=request.user.id)

    pendingSched = sched.filter(status="Pending")
    onGoingSched = sched.filter(status="On Going")
    doneSched = sched.filter(status="Done")
    approvedSched = sched.filter(status="Approved")
    rejectedSched = sched.filter(status="Rejected")

    # pendingSchedPaginator = Paginator(pendingSched, 5)
    # page_number = request.GET.get('page')
    # pendingSchedPage_obj = pendingSchedPaginator.get_page(page_number)

    # onGoingSchedPaginator = Paginator(onGoingSched, 5)
    # page_number = request.GET.get('page')
    # onGoingSchedPage_obj = onGoingSchedPaginator.get_page(page_number)

    # doneSchedPaginator = Paginator(doneSched, 5)
    # page_number = request.GET.get('page')
    # doneSchedPage_obj = doneSchedPaginator.get_page(page_number)

    # approvedSchedPaginator = Paginator(approvedSched, 5)
    # page_number = request.GET.get('page')
    # approvedSchedPage_obj = approvedSchedPaginator.get_page(page_number)

    # rejectedSchedPaginator = Paginator(rejectedSched, 5)
    # page_number = request.GET.get('page')
    # rejectedSchedPage_obj = rejectedSchedPaginator.get_page(page_number)

    context = {
        'pendingSched': pendingSched,
        'onGoingSched': onGoingSched,
        'doneSched': doneSched,
        'approvedSched': approvedSched,
        'rejectedSched': rejectedSched,
        'sched': sched
    }



    return render(request, './account/prof/profDashboard.html', context)