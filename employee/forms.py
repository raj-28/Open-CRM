from django import forms
from django.contrib.auth.models import User
from . import models





#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class HrUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class HrForm(forms.ModelForm):
    class Meta:
        model=models.Hr
        fields=['email','mobile','status','department','designation']



#for employee related form
class EmployeeUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class EmployeeForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it

    class Meta:
        model=models.Employee
        fields=['email','mobile','status','department','designation']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Employee
        fields = ['profile_pic']
class ProfileUpdateFormforHr(forms.ModelForm):

    class Meta:
        model = models.Hr
        fields = ['profile_pic']

class taskmediaForm(forms.ModelForm):

    class Meta:
        model = models.Task_Media
        fields = ['media',]
