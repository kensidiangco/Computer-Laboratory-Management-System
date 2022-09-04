from contextlib import redirect_stderr
from urllib.robotparser import RequestRate
from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from ...decorators import unauthenticated_user, admin_only, ITDept_only
from django.contrib.auth.models import Group
from .models import Theme
from ..transaction.models import Sched_Request
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            user.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            
            messages.success(request, 'Account successfully created for ' + username)
            return HttpResponseRedirect(reverse('loginPage'))
            
        else:
            messages.error(request, form.errors)
            
    return render(request, './account/register.html', { 'registerForm': form })
    
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
            
    return render(request, './account/ITDeptAccountRegister.html', { 'registerForm': form })

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('adminDashboard'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.error(request, 'Check your password!')
            
    return render(request, './account/login.html')

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
@admin_only
def formPage(request):
    return render(request, './account/forms.html')
    
@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def adminDashboard(request):
    schedReqs = Sched_Request.objects.all()

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color,
        'schedReqs': schedReqs
    }
    return render(request, './account/admin/dashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
@ITDept_only
def ITDeptDashboard(request):
    return render(request, './account/itdept/dashboard.html')

@login_required(login_url=reverse_lazy("loginPage"))
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    
@login_required(login_url=reverse_lazy("loginPage"))
def userPage(request):
    return render(request, './account/userPage.html')