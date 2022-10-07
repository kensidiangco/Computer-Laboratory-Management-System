from django.views import View
import xlwt
import io
import xlsxwriter
from xhtml2pdf import pisa
import pandas as pd
from datetime import datetime, date, time
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from CLMS.apps.account.models import Notification
from .models import Approved_Schedule, Rejected_Schedule, Student, Sched_Request, Sched_Time_Usage
from django.http import JsonResponse 
from .forms import ScheduleRequestForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string

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

            subject = "New Schedule Request!"
            email_template_name = "transaction/notification/email/email_notification_template.txt"
            c = {
                "email":"kensidiangco@gmail.com",
                'domain':'127.0.0.1:8000',
                'site_name': 'Website',
                'protocol': 'http',
                'sched_date_req': sched.date_request,
                'sched': sched.pk
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'admin@example.com' , ['kensidiangco@gmail.com', 'jore.sidiangco.sjc@phinmaed.com', 'nisu.marcelo.sjc@phinmaed.com', 'jhpa.carag.sjc@phinmaed.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

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

    dateTimeA = datetime.combine(datetime.today(), requestDetails.time_in)
    dateTimeB = datetime.combine(datetime.today(), requestDetails.time_out)

    dateTimeDifference = dateTimeB - dateTimeA
    dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 3600

    print(dateTimeDifferenceInHours, dateTimeDifference)

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
    totalUnread = Notification.objects.filter(read=False, receiver=request.user).count()

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

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = io.BytesIO()
	pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def Prof_Pending_Schedule(request):
    scheds = Sched_Request.objects.filter(requester=request.user, status="Pending").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/prof_view/pending_schedule.html', context)

def Prof_Approved_Schedule(request):
    scheds = Sched_Request.objects.filter(requester=request.user, status="Approved").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/prof_view/approved_schedule.html', context)

def Prof_Rejected_Schedule(request):
    scheds = Sched_Request.objects.filter(requester=request.user, status="Rejected").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/prof_view/rejected_schedule.html', context)

def Prof_Ongoing_Schedule(request):
    scheds = Sched_Request.objects.filter(requester=request.user, status="On Going").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/prof_view/ongoing_schedule.html', context)

def Prof_Done_Schedule(request):
    scheds = Sched_Request.objects.filter(requester=request.user, status="Done").order_by('date_created')
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    schedCount = len(scheds)
    context = {
        'scheds': scheds,
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/prof_view/done_schedule.html', context)

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        data = {
            'data': Sched_Request.objects.filter(status="Done"),
            'date_today': datetime.today().strftime('%B %d, %Y %I:%H %p')
        }
        pdf = render_to_pdf('pdf/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        data = {
            'data': Sched_Request.objects.filter(status="Done"),
            'date_today': datetime.today().strftime('%B %d, %Y %I:%H %p')
        }
        pdf = render_to_pdf('app/pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "CLSM-Schedules%s.pdf" %(datetime.today().strftime('%B %d, %Y %I:%H %p'))
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response

def exportData(request):
    scheds = Sched_Request.objects.all()

    if request.method == "POST":
        DateFrom = request.POST.get('dateFrom')
        DateTo = request.POST.get('dateTo')
        sched_status = request.POST.get('sched_status')
        if sched_status == "all":
            queryset = Sched_Request.objects.filter(date_request__range=[DateFrom, DateTo])
        else:
            queryset = Sched_Request.objects.filter(date_request__range=[DateFrom, DateTo], status=sched_status)

        data = {
            'data': queryset,
            'date_today': datetime.today().strftime('%B %d, %Y'),
            'DateFrom': DateFrom,
            'DateTo': DateTo
        }
        pdf = render_to_pdf('pdf/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


        # DateFrom = request.POST.get('dateFrom')
        # DateTo = request.POST.get('dateTo')
        # queryset = Sched_Request.objects.filter(date_request__range=[DateFrom, DateTo], status="Done")

        # response = HttpResponse(content_type='application/ms-excel')
        # response['Content-Disposition'] = 'attachment; filename="Done-Schedules.xls"'

        # wb = xlwt.Workbook(encoding='utf-8')
        # ws = wb.add_sheet('Done schedules')

        # # Sheet header, first row
        # row_num = 0

        # font_style = xlwt.XFStyle()
        # font_style.font.bold = True

        # columns = ['requester', 'course', 'year_level', 'section', 'time_in', 'time_out', 'date_request', 'status', 'date_created']

        # for col_num in range(len(columns)):
        #     ws.write(row_num, col_num, columns[col_num], font_style)

        # # Sheet body, remaining rows
        # font_style = xlwt.XFStyle()

        # rows = queryset.values_list('requester__username', 'course', 'year_level', 'section', 'time_in', 'time_out', 'date_request', 'status', 'date_created')
        # for row in rows:
        #     row_num += 1
        #     for col_num in range(len(row)):
        #         if isinstance(row[col_num], date):
        #             dateCol = row[col_num].strftime('%Y-%m-%d')
        #             ws.write(row_num, col_num, dateCol, font_style)
        #         elif isinstance(row[col_num], time):
        #             timeCol = row[col_num].strftime('%I:%M %p')
        #             ws.write(row_num, col_num, timeCol, font_style)
        #         else:
        #             ws.write(row_num, col_num, row[col_num], font_style)

        # wb.save(response)
        # return response

    paginator = Paginator(scheds, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    schedCount = len(scheds)

    context = {
        'page_obj': page_obj,
        'schedCount': schedCount
    }

    return render(request, './transaction/exportData.html', context)