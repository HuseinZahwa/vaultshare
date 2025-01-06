# ///////////////////////////////////////////////////////////////////////////
# // File Name: forms.py
# // Group Number: Group 9
# // Group Members Names : Husein Zahwa
# // Group Members Seneca Email : hnzahwa@myseneca.ca
# // Date : November 19, 2024
# // Authenticity Declaration :
# // I declare this submission is the result of my group work and has not been
# // shared with any other groups/students or 3rd party content provider. This submitted
# // piece of work is entirely of my own creation.
# //////////////////////////////

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Extending Django's built-in UserCreationForm to include an email field
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] # Defining fields for user creation


class UploadFileForm(forms.Form):
    file = forms.FileField(required = False) # Allowing the user to submit a FileField form with no file
                                             # Was done to test the messages.error Django feature  