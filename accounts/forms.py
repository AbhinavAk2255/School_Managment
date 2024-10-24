from typing import Any
from django import forms
from .models import *
from django.core.validators import MinLengthValidator
from django.forms import EmailInput, Form, Select, CheckboxInput,CharField, ChoiceField
from django.forms import TextInput, PasswordInput, Textarea, FileInput, DateInput
from django.contrib.auth.forms import UserCreationForm

#user registration

class UserRegistrationForm(forms.ModelForm):
    confirm_password = CharField(
        max_length = 25,
        min_length = 8,
        required = True,
        validators = [
            MinLengthValidator(8, 'The password is too short.')
        ],
        widget = PasswordInput({
            'class': 'form-control'
        }),
        label='Confirm Password'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        
        widgets = {
            'username': TextInput({
                'class': 'form-control',
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'password': PasswordInput({
                'class': 'form-control'
            }),


        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
    


class LoginForm(Form):
    username = CharField(
        max_length = 15,
        min_length = 4,
        required = True,
        widget = TextInput({
            'class': 'form-control',
            'placeholder':'Username'
        })
    )

    password = CharField(
        max_length = 15,
        min_length = 4,
        required = True,
        widget = PasswordInput({
            'class': 'form-control',
            'placeholder':'Password'
        })
    )


# Forgot Password Email Form 
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )



# Reset Password Form
class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    


# Profile Update
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

        widgets = {
            'username': TextInput({
                'class': 'form-control'
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'profile_photo', 'dob', 'location']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }



class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'role', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'




class UpdateLibraryHistoryForm(forms.ModelForm):
    class Meta:
        model=LibraryHistory
        fields='__all__'
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
              
        }
        
    def __init__(self, *args, **kwargs):
        super(UpdateLibraryHistoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class FeeHistoryUpdateForm(forms.ModelForm):
    class Meta:
        model = FeesHistory
        fields='__all__'
        
        widgets = {
              'payment_date': forms.DateInput(attrs={'type': 'date'}),
          }
        
    def __init__(self, *args, **kwargs):
        super(FeeHistoryUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'



class AddBookForm(forms.ModelForm):
    class Meta:
        model = Library
        fields='__all__'
        
        
    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'