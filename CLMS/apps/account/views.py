from typing import ContextManager
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from ...decorators import dean_only, unauthenticated_user, admin_only, ITDept_only, prof_only
from django.contrib.auth.models import Group
from .models import Notification, Theme, Profile
from ..transaction.models import Sched_Request
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from datetime import datetime

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "account/password/password_reset_email.txt"
					c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                        
                    # messages.success(request, "A message with reset password instructions has been sent to your inbox.")
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="account/password/password_reset.html", context={"password_reset_form":password_reset_form})

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

@login_required(login_url=reverse_lazy("loginPage"))
def profile(request):
    return render(request, './account/profile.html')

@login_required(login_url=reverse_lazy("loginPage"))
def index(request):

    if Theme.objects.filter(user=request.user.username).exists():
        color = Theme.objects.get(user=request.user.username).color
    else:
        color = 'light'
        
    context = {
        'color': color
    }

    return render(request, './index.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
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
    active_user = User.objects.all()

    context = {
        'active_user': active_user
    }
    return render(request, './account/forms.html', context)
    
@login_required(login_url=reverse_lazy("loginPage"))
@admin_only
def adminDashboard(request):
    pending = Sched_Request.objects.filter(status="Pending")
    approved = Sched_Request.objects.filter(status="Approved")
    rejected = Sched_Request.objects.filter(status="Rejected")
    onGoing = Sched_Request.objects.filter(status="On going")
    done = Sched_Request.objects.filter(status="Done")

    date_today = datetime.today().strftime('%B %d, %Y %H:%M:%p')
    scheds = Sched_Request.objects.filter(status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)

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
        'done': done,
        'date_today': date_today,
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount,
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

    date_today = datetime.today().strftime('%B %d, %Y %H:%M:%p')
    scheds = Sched_Request.objects.filter(status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)

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
        'done': done,
        'date_today': date_today,
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
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
    
    date_today = datetime.today().strftime('%B %d, %Y %H:%M:%p')
    scheds = Sched_Request.objects.filter(status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)

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
        'done': done,
        'date_today': date_today,
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }
    return render(request, './account/itdept/dashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url=reverse_lazy("loginPage"))
@prof_only
def profDashboard(request):
    sched = Sched_Request.objects.filter(requester=request.user)

    pendingSched = sched.filter(status="Pending")
    onGoingSched = sched.filter(status="On Going")
    doneSched = sched.filter(status="Done")
    approvedSched = sched.filter(status="Approved")
    rejectedSched = sched.filter(status="Rejected")

    scheds = Sched_Request.objects.filter(requester=request.user, status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    date_today = datetime.today().strftime('%B %d, %Y %H:%M:%p')

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
        'sched': sched,
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount,
        'date_today':date_today
    }
    return render(request, './account/prof/profDashboard.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def About_Us(request):
    return render(request, './about_us.html')

def notification_page(request):
    notifs = Notification.objects.filter(receiver=request.user).order_by('-date_created')

    if request.method == 'POST':
        if 'All' in request.POST:
            notifs = Notification.objects.filter(receiver=request.user).order_by('-date_created')
            notifs_count = Notification.objects.filter(receiver=request.user).order_by('-date_created').count
            return render(request, './account/notification.html', {
                'notifs': notifs,
                'notifs_count': notifs_count
            })


        if 'Unread' in request.POST:
            notifs = Notification.objects.filter(receiver=request.user, read=False).order_by('-date_created')
            notifs_count = Notification.objects.filter(receiver=request.user, read=False).order_by('-date_created').count
            return render(request, './account/notification.html', {
                'notifs': notifs,
                'notifs_count': notifs_count
            })

    else:
        context = {
            'notifs': notifs
        }

        return render(request, './account/notification.html', context)