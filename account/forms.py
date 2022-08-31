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
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder':'Last Name',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
            }),
            'username': forms.TextInput(attrs={
                'placeholder':'Username',
                'class': 'rounded-md transition transition-delay-2',
                'autocapitalize':'none',
                'id':'username',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'placeholder':'Email',
                'class': 'rounded-md transition transition-delay-2',
                'required': '',
      }),
    }
    
    def __init__(self, *args, **kwargs):
        
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': ("New password"),
            'class': ("rounded-md transition transition-delay-2"),
        })
        
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': ("Confirm password"),
            'class': ("rounded-md transition transition-delay-2"),
        })