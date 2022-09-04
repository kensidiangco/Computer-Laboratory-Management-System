from msilib.schema import File
from django.shortcuts import render
from .models import Student, Sched_Request
import pandas as pd
from django.http import JsonResponse 
from .forms import ScheduleRequestForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse_lazy
from django.core.paginator import Paginator

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

    schedForm = ScheduleRequestForm()
    studentForm = StudentForm()
    return render(request, './transaction/requestForm.html', {
        'schedForm': schedForm,
        'studentForm': studentForm,
    })

def requestList(request):
    scheds = Sched_Request.objects.all()
    paginator = Paginator(scheds, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'scheds': scheds,
        'page_obj': page_obj
    }

    return render(request, './transaction/requests.html', context)

@login_required(login_url=reverse_lazy("loginPage"))
def requestDetails(request, pk):
    requestDetails = Sched_Request.objects.get(pk=pk)
    students = requestDetails.student_set.all()
    paginator = Paginator(students, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, './transaction/requestDetails.html', {'requestDetails': requestDetails, 'page_obj': page_obj})