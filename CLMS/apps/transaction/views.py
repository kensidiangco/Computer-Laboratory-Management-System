from datetime import datetime
from msilib.schema import File
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers

from CLMS.apps.account.models import Notification
from .models import Approved_Schedule, Rejected_Schedule, Student, Sched_Request, Sched_Time_Usage
import pandas as pd
from django.http import JsonResponse 
from .forms import ScheduleRequestForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User

import io
import xlsxwriter
from django.http import HttpResponse


@login_required(login_url=reverse_lazy("loginPage"))
def studentListExport(request):
# create our spreadsheet.  I will create it in memory with a StringIO
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    cell_format = workbook.add_format({'bold': True, 'align': 'center'})
    worksheet.set_column('A:G', 20)

    worksheet.write('A1', 'student_no', cell_format)
    worksheet.write('B1', 'first_name', cell_format)
    worksheet.write('C1', 'last_name', cell_format)
    worksheet.write('D1', 'middle_name', cell_format)
    worksheet.write('F1', 'email', cell_format)
    worksheet.write('E1', 'contact', cell_format)
    worksheet.write('G1', 'address', cell_format)
    workbook.close()
    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="student_class_info.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response
    
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
                receiver=User.objects.get(username='dean'),
                sender=request.user,
                notif_for='schedule',
                description='New schedule request',
                sched_url=sched.pk
            )

            Notification.objects.create(
                receiver=User.objects.get(username='itdept'),
                sender=request.user,
                notif_for='schedule',
                description='New schedule request',
                sched_url=sched.pk
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

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/requestList.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def requestDetails(request, pk):
    requestDetails = get_object_or_404(Sched_Request, pk=pk)
    
    group = list(request.user.groups.values_list('name', flat = True))
    
    students = requestDetails.student_set.all().order_by("last_name")
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    approvedId = Approved_Schedule.objects.filter(sched=requestDetails)

    if request.method == 'POST':
        if 'approve_sched' in request.POST:
            sched = Sched_Request.objects.get(pk=pk)

            approved = Approved_Schedule.objects.create(
                approved_by = request.user,
                sched = sched
            )
            approved.save()

            requestDetails.status="Approved"
            requestDetails.save()

            time_usage = Sched_Time_Usage.objects.create(
                sched=approvedId.first()
            )
            time_usage.save()

            Notification.objects.create(
                receiver=User.objects.get(username=sched.requester.username),
                sender=request.user,
                notif_for='schedule',
                description='Your request for {} is approved by {}'.format(sched.date_request, request.user),
                sched_url=sched.pk
            )

            Notification.objects.create(
                receiver=User.objects.get(username='itdept'),
                sender=request.user,
                notif_for='schedule',
                description='{} schedule requested is approved by {}'.format(sched.date_request, request.user),
                sched_url=sched.pk
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
                description='Your request for {} is rejected by {}'.format(sched.date_request, request.user),
                sched_url=sched.pk
            )

            Notification.objects.create(
                receiver=User.objects.get(username='itdept'),
                sender=request.user,
                notif_for='schedule',
                description='{} schedule requested is rejected by {}'.format(sched.date_request, request.user),
                sched_url=sched.pk
            )

        if 'timein' in request.POST:
            sched = Sched_Request.objects.get(pk=pk)
            timein = Sched_Time_Usage.objects.get(sched=approvedId.first())
            timein.time_in = datetime.now().time()
            timein.save()

            requestDetails.status="On Going"
            requestDetails.save()
            # Sched_Time_Usage.objects.create(
            #     sched = approvedId.first()
            # )
            
            # requestDetails.status="On going"
            # requestDetails.save()

            Notification.objects.create(
                receiver=User.objects.get(username='itdept'),
                sender=request.user,
                notif_for='schedule',
                description='{} has occupied comlab as of {}'.format(request.user, datetime.now().strftime("%B %d, %Y at %H:%M")),
                sched_url=sched.pk
            )

            Notification.objects.create(
                receiver=User.objects.get(username='dean'),
                sender=request.user,
                notif_for='schedule',
                description='{} has occupied comlab as of {}'.format(request.user, datetime.now().strftime("%B %d, %Y at %H:%M")),
                sched_url=sched.pk
            )
        
        if 'timeout' in request.POST:
            sched = Sched_Request.objects.get(pk=pk)
            timeout = Sched_Time_Usage.objects.get(sched=approvedId.first())
            timeout.time_out = datetime.now().time()
            timeout.save()

            requestDetails.status="Done"
            requestDetails.save()

            Notification.objects.create(
                receiver=User.objects.get(username='itdept'),
                sender=request.user,
                notif_for='schedule',
                description='{} left the comlab at {}'.format(request.user, datetime.now().strftime("%H:%M")),
                sched_url=sched.pk
            )

            Notification.objects.create(
                receiver=User.objects.get(username='dean'),
                sender=request.user,
                notif_for='schedule',
                description='{} left the comlab at {}'.format(request.user, datetime.now().strftime("%H:%M")),
                sched_url=sched.pk
            )

    try:
        time_usage = Sched_Time_Usage.objects.get(sched=approvedId.first())
        context = {
            'requestDetails': requestDetails,
            'page_obj': page_obj, 
            'group': group,
            'time_usage': time_usage
        }
        return render(request, './transaction/requestDetails.html', context)
    except:
        context = {
            'requestDetails': requestDetails,
            'page_obj': page_obj, 
            'group': group,
        }
        return render(request, './transaction/requestDetails.html', context)

def approvedRequest(request):
    approved = Sched_Request.objects.filter(status='Approved').order_by('date_created')
    schedCount = len(approved)
    paginator = Paginator(approved, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'approved': approved,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/approvedRequest.html', context)

def rejectedRequest(request):
    rejected = Sched_Request.objects.filter(status='Rejected').order_by('date_created')
    schedCount = len(rejected)
    paginator = Paginator(rejected, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'rejected': rejected,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/rejectedRequest.html', context)
    
def getNotifs(request):
    data = Notification.objects.filter(receiver=request.user).order_by('-date_created')
    jsonData = serializers.serialize('json', data)
    totalUnread = Notification.objects.filter(read=False).count()

    return JsonResponse({'data': jsonData, 'totalUnread': totalUnread})

def clearNotification(request):
    notifications = Notification.objects.filter(read=False, receiver=request.user) 
    notifications.update(read=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def onGoingSchedule(request):
    onGoing = Sched_Request.objects.filter(status="On Going")
    schedCount = len(onGoing)
    paginator = Paginator(onGoing, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'onGoing': onGoing,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/onGoingSchedule.html', context)

def doneSchedule(request):
    doneSched = Sched_Request.objects.filter(status="Done")

    paginator = Paginator(doneSched, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    schedCount = len(doneSched)

    context = {
        'doneSched': doneSched,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/doneSchedule.html', context)