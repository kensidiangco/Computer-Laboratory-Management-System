from datetime import datetime
from msilib.schema import File
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse

from CLMS.apps.account.models import Notification
from .models import Approved_Schedule, Rejected_Schedule, Student, Sched_Request, Sched_Time_Usage
import pandas as pd
from django.http import JsonResponse 
from .forms import SchedStatusForm, ScheduleRequestForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User

@login_required(login_url=reverse_lazy("loginPage"))
def studentListExport(request):
    students = Student.objects.all()
    data = []

    for obj in students:
        data.append({
            "student_no": obj.student_no,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "middle_name": obj.middle_name,
            "email": obj.email,
            "contact": obj.contact,
            "address": obj.address,
        })

    pd.DataFrame(data).to_excel('students.xlsx')

    return JsonResponse({
        'status' : 200
    })

def transactionIndexPage(request):
    return render(request, './transaction/index.html')

@login_required(login_url=reverse_lazy("loginPage"))
def requestForm(request):
    if request.method == 'POST':
        schedForm = ScheduleRequestForm(request.POST)
        file = request.FILES['files']
        df = pd.read_excel(file)

        if schedForm.is_valid():
            sched = schedForm.save(commit=False)
            sched.requester = request.user
            sched.class_list = file
            sched.save()

            Notification.objects.create(
                receiver=User.objects.get(username='ken'),
                sender=request.user,
                notif_for='schedule',
                description='New schedule request'
            )
            
            for element in df.to_dict('records'):
                Student.objects.create(
                    sched = sched,
                    student_no = element['student_no'],
                    first_name= element['first_name'],
                    last_name= element['last_name'],
                    middle_name= element['middle_name'],
                    contact= element['contact'],
                    email= element['email'],
                    address= element['address']
                )

            return redirect('requestDetails', pk=sched.pk)

    schedForm = ScheduleRequestForm()
    studentForm = StudentForm()
    return render(request, './transaction/requestForm.html', {
        'schedForm': schedForm,
        'studentForm': studentForm,
    })

def requestList(request):
    scheds = Sched_Request.objects.filter(status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'scheds': scheds,
        'page_obj': page_obj
    }

    return render(request, './transaction/requestList.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def requestDetails(request, pk):
    requestDetails = get_object_or_404(Sched_Request, pk=pk)

    group = list(request.user.groups.values_list('name',flat = True))
    students = requestDetails.student_set.all().order_by("last_name")
    paginator = Paginator(students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    approvedId = Approved_Schedule.objects.filter(sched=requestDetails)

    if request.method == 'POST':
        if 'approve_sched' in request.POST:
            sched = Sched_Request.objects.get(pk=pk)
            Approved_Schedule.objects.create(
                approved_by = request.user,
                sched = sched
            )
            requestDetails.status="Approved"
            requestDetails.save()

            Notification.objects.create(
                receiver=User.objects.get(username=sched.requester.username),
                sender=request.user,
                notif_for='schedule',
                description='Your request for {} is approved'.format(sched.date_request)
            )
        
        if 'reject_sched' in request.POST:
            sched = Sched_Request.objects.get(pk=pk)
            Rejected_Schedule.objects.create(
                rejected_by = request.user,
                sched = sched
            )
            requestDetails.status="Rejected"
            requestDetails.save()
        
            Notification.objects.create(
                receiver=User.objects.get(username=sched.requester.username),
                sender=request.user,
                notif_for='schedule',
                description='Your request for {} is approved'.format(sched.date_request)
            )

        if 'timein' in request.POST:
            Sched_Time_Usage.objects.create(
                sched = approvedId.first()
            )
            
            requestDetails.status="On going"
            requestDetails.save()

            Notification.objects.create(
                receiver=User.objects.get(username='ken'),
                sender=request.user,
                notif_for='schedule',
                description='{} has occupied comlab as of {}'.format(request.user, datetime.now().strftime("%B %d, %Y at %H:%M"))
            )
        
        if 'timeout' in request.POST:
            Sched_Time_Usage.objects.create(
                sched = approvedId.first(),
                time_out = datetime.now().time()
            )

            requestDetails.status="Done"
            requestDetails.save()

            Notification.objects.create(
                receiver=User.objects.get(username='ken'),
                sender=request.user,
                notif_for='schedule',
                description='{} left the comlab at {}'.format(request.user, datetime.now().strftime("%H:%M"))
            )

    return render(request, './transaction/requestDetails.html', {'requestDetails': requestDetails, 'page_obj': page_obj, 'group': group})

def approvedRequest(request):
    approved = Sched_Request.objects.filter(status='Approved').order_by('date_created')

    paginator = Paginator(approved, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'approved': approved,
        'page_obj': page_obj
    }

    return render(request, './transaction/approvedRequest.html', context)

def rejectedRequest(request):
    rejected = Sched_Request.objects.filter(status='Rejected').order_by('date_created')

    paginator = Paginator(rejected, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'rejected': rejected,
        'page_obj': page_obj
    }

    return render(request, './transaction/rejectedRequest.html', context)