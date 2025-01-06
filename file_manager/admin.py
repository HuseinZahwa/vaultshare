# ///////////////////////////////////////////////////////////////////////////
# // File Name: admin.py
# // Group Number: Group 9
# // Group Members Names : Husein Zahwa
# // Group Members Seneca Email : hnzahwa@myseneca.ca
# // Date : November 19, 2024
# // Authenticity Declaration :
# // I declare this submission is the result of my group work and has not been
# // shared with any other groups/students or 3rd party content provider. This submitted
# // piece of work is entirely of my own creation.
# //////////////////////////////

from django.contrib import admin

# Register your models here.
from .models import UserFile


# Creating a customizable admin panel to view the user, file name, and upload timestamp.
@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'uploaded_at') # Specify the panel to show the user, file, and uploaded_at (timestamp)
