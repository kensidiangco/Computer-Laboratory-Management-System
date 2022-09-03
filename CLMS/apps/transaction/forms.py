from django import forms
from .models import Sched_Request, Student
from datetime import datetime

now = datetime.now()
class ScheduleRequestForm(forms.ModelForm):
    class Meta():
        model = Sched_Request
        fields = ('course', 'year_level', 'section', 'schedule_in', 'schedule_out')
        widgets = {
            'course': forms.TextInput(attrs={
                'placeholder':'Course',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'year_level': forms.TextInput(attrs={
                'placeholder':'Year_level',
                'class': 'rounded-md transition transition-delay-2',
                'autocapitalize':'none',
                'id':'username',
            }),
            'section': forms.TextInput(attrs={
                'type': 'text',
                'placeholder':'Section',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'schedule_in': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder':'Schedule_in',
                'class': 'rounded-md transition transition-delay-2',
                'min': str(now.strftime('%Y-%m-%dT%H:%M:00')),
                'required': '',
            }, format='%Y-%m-%d %H:%M:%S'),
            'schedule_out': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder':'Schedule_out',
                'class': 'rounded-md transition transition-delay-2',
                'min': str(now.strftime('%Y-%m-%dT%H:%M:00')),
                'required': '',
            }, format='%Y-%m-%d %H:%M:%S'),
        }

class StudentForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('student_no', 'first_name', 'last_name', 'middle_name', 'contact', 'email', 'address')
        widgets = {
            'student_no': forms.TextInput(attrs={
                'placeholder':'student_no',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder':'first_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'last_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder':'middle_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'placeholder':'email',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'contact': forms.TextInput(attrs={
                'placeholder':'contact',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'address': forms.TextInput(attrs={
                'placeholder':'address',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            })
        }