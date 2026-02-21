from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from phonenumber_field.formfields import SplitPhoneNumberField 



class LoginForm(AuthenticationForm):
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = "Email"
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']
        

class UserUpdateForm(forms.ModelForm):
    phone_number = SplitPhoneNumberField(required=False, label="Phone Number")
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','email', 'address']


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            
            if name != 'phone_number':
                field.widget.attrs.update({'class': 'form-control'})

        phone_field = self.fields['phone_number']
        
        # Check if the widget has sub-widgets (Dropdown + Input)
        if hasattr(phone_field.widget, 'widgets'):
            # Style the Dropdown (Country Code)
            phone_field.widget.widgets[0].attrs.update({ # type: ignore
                'class': 'form-select',
                'style': 'width: 110px;'
            })
            
            # Style the Text Input (Phone Number)
            phone_field.widget.widgets[1].attrs.update({ # type: ignore
                'class': 'form-control',
                'type':'tel',
                'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
            })
        
        if 'email' in self.fields:
            self.fields['email'].disabled = True