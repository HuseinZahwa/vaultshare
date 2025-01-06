# ///////////////////////////////////////////////////////////////////////////
# // File Name: urls.py
# // Group Number: Group 9
# // Group Members Names : Husein Zahwa
# // Group Members Seneca Email : hnzahwa@myseneca.ca
# // Date : November 19, 2024
# // Authenticity Declaration :
# // I declare this submission is the result of my group work and has not been
# // shared with any other groups/students or 3rd party content provider. This submitted
# // piece of work is entirely of my own creation.
# //////////////////////////////

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Application's Home Page
    path('register/', views.register_view, name='register'),  # User Registration Page
    path('login/', views.login_view, name='login'),  # User Login Page
    path('logout/', views.logout_view, name='logout'),  # User Logout Page (redirects to login page)
    path('dashboard/', views.dashboard_view, name='dashboard'),  # User Dashboard Page
    path('upload/', views.upload_file_view, name='upload_file'),  # File Upload Page
    path('view_files/', views.view_files_view, name='view_files'),  # Page to View Uploaded Files
    path('download/<int:file_id>/', views.download_file_view, name='download_file'),  # File Download via Dynamic URL
    path('shared_download/<int:file_id>/', views.shared_download_view, name='shared_download'),
    path('shared_files/', views.shared_files_view, name='shared_files'),  # Page to View Shared Files
]

