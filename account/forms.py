from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('first_name', 'last_name','username','email','password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder':'First Name',
                'class': 'form-control form-control-user',
                'required': '',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'Last Name',
                'class': 'form-control form-control-user',
                'required': '',
            }),
            'username': forms.TextInput(attrs={
                'placeholder':'Username',
                'class': 'form-control form-control-user',
                'autocapitalize':'none',
                'id':'username',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'placeholder':'Email',
                'class': 'form-control',
                'required': '',
      }),
    }
    
    def __init__(self, *args, **kwargs):
        
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': ("New password"),
            'class': ("form-control form-control-user"),
        })
        
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': ("Confirm password"),
            'class': ("form-control form-control-user"),
        })