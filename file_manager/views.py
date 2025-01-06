# ///////////////////////////////////////////////////////////////////////////
# // File Name: views.py
# // Group Number: Group 9
# // Group Members Names : Husein Zahwa
# // Group Members Seneca Email : hnzahwa@myseneca.ca
# // Date : November 19, 2024
# // Authenticity Declaration :
# // I declare this submission is the result of my group work and has not been
# // shared with any other groups/students or 3rd party content provider. This submitted
# // piece of work is entirely of my own creation.
# //////////////////////////////


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, UploadFileForm
from .models import UserFile
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.core import signing
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
import os

# Generates an encrypted ID for a file based on its file_id
def generate_encrypted_id(file_id):
    return signing.dumps({'file_id': file_id}) # Using signing.dumps to generates an encrypted ID file using the automatically generated SECRET_KEY value

# Decodes an encrypted ID to retrieve the original file_id
def get_file_id_from_encrypted(encrypted_id):
    try:
        data = signing.loads(encrypted_id) # Decode the encrypted ID using signing.loads
        return data['file_id'] # Return the file_id if the encrypted ID is valid   
    except signing.BadSignature:
        return None # Return None if the encrypted ID is not valid

# Renders the home page of the application
def home_view(request):
    return render(request, 'file_manager/home.html') # Renders the home page

# Renders the register page of the application
def register_view(request):
    form = CreateUserForm()  # Initializes the user creation form
    if request.method == 'POST':  # Checks if the request method is POST
        form = CreateUserForm(request.POST)  # Populates the form with submitted data
        if form.is_valid():  # Checks the form input
            form.save()  # Saves the new user to the database
            user = form.cleaned_data.get('username')  # Extracts the username from the form
            messages.success(request, f'Account was created for {user}')  # Adds a success message with the username
            return redirect('login')  # Redirects the user to the login page
    context = {'form': form}  # Passes the form to the template
    return render(request, 'file_manager/register.html', context)  # Renders the register page

# Renders the login page of the application
def login_view(request):
    if request.method == 'POST':  # Checks if the request method is POST
        username = request.POST.get('username')  # Gets the username
        password = request.POST.get('password')  # Gets the password
        user = authenticate(request, username=username, password=password)  # Checks if the user exists in the database
        if user is not None:  # If the user exists
            login(request, user)  # Passes the user info to the built-in login method
            return redirect('dashboard')  # Redirects the user to the dashboard page
        else:  # If the user doesn't exist
            messages.info(request, "Invalid username or password")  # Displays an error message
    return render(request, 'file_manager/login.html')  # Renders the login page

# Renders the logout page (redirects to the login page)
def logout_view(request):
    logout(request) # Send the request to the built-in logout method
    messages.success(request, 'You have successfully logged out') # Display a success message
    return render(request, 'file_manager/login.html') # Renders the login page after logout


# Renders the dashboard page
@login_required # Ensures that only authenticated users can access this view
def dashboard_view(request):
    return render(request, 'file_manager/dashboard.html') # Renders the dashboard page


# Renders the upload page (upload file)
@login_required # Ensures that only authenticated users can access this view
def upload_file_view(request):
    form = UploadFileForm()  # Initialize the upload file form
    if request.method == 'POST':  # Check if the request method is POST
        form = UploadFileForm(request.POST, request.FILES)  # Populate the form with submitted data
        if not request.FILES.get('file'):  # If no file is selected
            messages.error(request, "Please select a file to upload")  # Display an error message
        elif form.is_valid():  # Validate the form input
            file = request.FILES['file']  # Extract the uploaded file
            UserFile.objects.create(user=request.user, file=file)  # Save the file to the database
            messages.success(request, f"The file '{file.name}' was uploaded successfully")  # Display a success message
        else:  # Handle invalid file
            messages.error(request, "Failed to upload file")  # Display an error message
    context = {'form': form}  # Pass the form to the template
    return render(request, 'file_manager/upload.html', context)  # Render the upload page


# Renders the view files page
@login_required # Ensures that only authenticated users can access this view
def view_files_view(request):
    files = UserFile.objects.filter(user=request.user)
    files_with_ids = [
        {
            'file': file,
            'download_url': request.build_absolute_uri(reverse('download_file', args=[file.id])),
            'encrypted_id': generate_encrypted_id(file.id),
        }
        for file in files
    ]
    print(f"[DEBUG] files_with_ids: {files_with_ids}")  # Add this debug line
    context = {'files_with_ids': files_with_ids}
    return render(request, 'file_manager/view_files.html', context)



# Renders the download page (downloads a file, more like an action than a page)
@login_required
def download_file_view(request, file_id):
    try:
        file_instance = get_object_or_404(UserFile, id=file_id)
        file_path = file_instance.file.path

        if not os.path.exists(file_path):
            messages.error(request, "File does not exist.")
            return redirect('view_files')

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={file_instance.file.name}'
            return response
    except Exception:
        messages.error(request, "An error occurred while trying to download the file.")
        return redirect('view_files')


# Renders the shared files view page
@login_required # Ensures that only authenticated users can access this view
def shared_files_view(request):
    file = None
    if request.method == 'POST':  # Check if the request method is POST
        encrypted_id = request.POST.get('encrypted_id')  # Get the encrypted ID from the form
        if encrypted_id:  # Check if an ID was submitted
            file_id = get_file_id_from_encrypted(encrypted_id)  # Decode the encrypted ID
            if file_id:  # If decoding was successful
                try:
                    file = UserFile.objects.get(id=file_id)  # Retrieve the file from the database
                    messages.success(request, "File found!")  # Set a success message
                except ObjectDoesNotExist:  # Handle file not found
                    messages.error(request, "Invalid ID or file not found.")  # Set an error message
            else:  # Handle decoding failure
                messages.error(request, "Invalid encrypted ID.")  # Set an error message
        else:  # Handle empty input
            messages.error(request, "Please enter an encrypted ID.")  # Set an error message
    return render(request, 'file_manager/shared_files.html', {'file': file})  # Render the template

# Renders the download page for shared files
@login_required # Ensures that only authenticated users can access this view
def shared_download_view(request, file_id): # Takes a file_id as an argument
    file_instance = get_object_or_404(UserFile, id=file_id) # Checks the database for a file with the provided file_id or returns a 404 error if not found
    file_path = file_instance.file.path # Retrieves the absolute file path of the file
    with open(file_path, 'rb') as f: # Opens the file in binary read mode using the file path
        response = HttpResponse(f.read(), content_type="application/octet-stream") # Creates an HTTP response with the file content; binary format ensures any file type is handled
        response['Content-Disposition'] = f'attachment; filename={file_instance.file.name}' # Specifies the content as an attachment and sets the download file name to match the original file name
        return response # Returns the HTTP response to initiate the file download

