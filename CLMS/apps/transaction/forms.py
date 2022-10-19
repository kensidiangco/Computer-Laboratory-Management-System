from django import forms
from .models import Computer_Lab, Sched_Request, Student
from datetime import datetime

now = datetime.now()

class ComLabSelect(forms.Select):
    def create_option(self, room, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(room, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['room'] = value.instance.room
        return option

class ScheduleRequestForm(forms.ModelForm):
    class Meta():
        model = Sched_Request
        fields = ('course', 'year_level', 'section', 'date_request', 'time_in', 'time_out', 'comlab_room')
        widgets = {
            'course': forms.TextInput(attrs={
                'placeholder':'Course',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'year_level': forms.TextInput(attrs={
                'placeholder':'Year level',
                'class': 'rounded-md transition transition-delay-2',
                'autocapitalize':'none',
                'id':'username',
                'required': True,

            }),
            'section': forms.TextInput(attrs={
                'type': 'text',
                'placeholder':'Section',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'date_request': forms.DateTimeInput(attrs={
                'type': 'date',
                'placeholder':'Schedule_in',
                'class': 'rounded-md transition transition-delay-2 w-full',
                'min': str(now.strftime('%Y-%m-%d')),
                'required': True,
            }, format='%Y-%m-%d'),
            'time_in': forms.DateTimeInput(attrs={
                'type': 'time',
                'placeholder':'Schedule_out',
                'class': 'rounded-md transition transition-delay-2 w-full',
                'required': True,
            }),
            'time_out': forms.DateTimeInput(attrs={
                'type': 'time',
                'placeholder':'Schedule_out',
                'class': 'rounded-md transition transition-delay-2 w-full',
                'required': True,
            }),
            'comlab_room': ComLabSelect(attrs={'class': "rounded-md transition transition-delay-2 w-full"}),
        }

class StudentForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ('student_no', 'first_name', 'last_name', 'middle_name', 'contact', 'email', 'address')
        widgets = {
            'student_no': forms.TextInput(attrs={
                'placeholder':'student_no',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder':'first_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'last_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder':'middle_name',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'placeholder':'email',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'contact': forms.TextInput(attrs={
                'placeholder':'contact',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'address': forms.TextInput(attrs={
                'placeholder':'address',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            })
        }

class SchedStatusForm(forms.ModelForm):
    class Meta():
        model = Sched_Request
        fields = ('status',)

class LaboratoryCreateForm(forms.ModelForm):
    class Meta:
        model = Computer_Lab
        fields = ('room', 'floor')
        widgets = {
            'room': forms.TextInput(attrs={
                'placeholder':'Room Name & No',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            }),
            'floor': forms.NumberInput(attrs={
                'placeholder':'Floor',
                'class': 'rounded-md transition transition-delay-2',
                'required': True,
            })
        }