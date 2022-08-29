from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .decorators import unauthenticated_user, admin_only, ITDept_only
from django.contrib.auth.models import Group

@unauthenticated_user
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

@unauthenticated_user
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
                return HttpResponseRedirect(reverse('adminIndex'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.error(request, 'Check your password!')
            
    return render(request, './account/login.html')

@login_required
@admin_only
def adminIndex(request):
    return render(request, './account/adminIndex.html')

@login_required
@ITDept_only
def ITDeptIndex(request):
    return render(request, './account/ITDeptIndex.html')

@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('adminIndex'))
    
@login_required
def userPage(request):
    return render(request, './account/userPage.html')