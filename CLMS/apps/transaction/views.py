from django.shortcuts import render
from .models import Student, Sched_Request, StudentListExcelFile
import pandas as pd
from django.http import JsonResponse 
from .forms import ScheduleRequestForm, StudentForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def studentListExport(request):
    students = Sched_Request.objects.all()
    data = []

    for obj in students:
        data.append({
            "student_no": obj.students.student_no,
            "first_name": obj.students.first_name,
            "last_name": obj.students.last_name,
            "middle_name": obj.students.middle_name,
            "email": obj.students.email,
            "contact": obj.students.contact,
            "address": obj.students.address,
        })

    pd.DataFrame(data).to_excel('students.xlsx')

    return JsonResponse({
        'status' : 200
    })

def transactionIndexPage(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, './transaction/index.html', context)

@login_required
def schedRequestPage(request):

    if request.method == 'POST':
        schedForm = ScheduleRequestForm(request.POST)
        file = request.POST.get('files', False)
        studentObj = StudentListExcelFile.objects.create(
            students = file
        )        
        path = str(studentObj.students)
        print(f'{settings.BASE_DIR}/{path}')
        df = pd.read_excel(path)

        if schedForm.is_valid():
            sched = schedForm.save(commit=False)
            sched.requester = request.user
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
    return render(request, './transaction/schedRequest.html', {
        'schedForm': schedForm,
        'studentForm': studentForm
    })