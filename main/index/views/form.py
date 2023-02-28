from django import forms
from .. import models

class UserForm(forms.Form):
    username = forms.CharField(label="Employee ID", max_length=128)
    password = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput)


class PasswordForm(forms.Form):
    old_password_flag = True
    old_password = forms.CharField(label="Old Password", min_length=8, widget=forms.PasswordInput())
    new_password = forms.CharField(label="New Password", min_length=8, widget=forms.PasswordInput()) 
    c = forms.CharField(label="Re-type New Password", min_length=8, widget=forms.PasswordInput())

    def set_old_password(self):
        self.old_password_flag =False
        return 0
    def clean_oldpassword(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')

        if not old_password:
            raise forms.ValidationError("Please Enter your Old Password.")

        if self.old_password_flag == False:
            raise forms.ValidationError("The old password is wrong.")

        return  old_password
