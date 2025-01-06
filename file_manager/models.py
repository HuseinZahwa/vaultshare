# ///////////////////////////////////////////////////////////////////////////
# // File Name: models.py
# // Group Number: Group 9
# // Group Members Names : Husein Zahwa
# // Group Members Seneca Email : hnzahwa@myseneca.ca
# // Date : November 15, 2024
# // Authenticity Declaration :
# // I declare this submission is the result of my group work and has not been
# // shared with any other groups/students or 3rd party content provider. This submitted
# // piece of work is entirely of my own creation.
# //////////////////////////////

from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.user.username}"


