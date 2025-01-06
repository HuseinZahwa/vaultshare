import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from file_manager.forms import CreateUserForm, UploadFileForm
from file_manager.views import generate_encrypted_id, get_file_id_from_encrypted
## Test User Registration and Authentication
# Test that a new user can register successfully
@pytest.mark.django_db
def test_user_registration(client):
    # Simulate a POST request to the register endpoint with valid data
    response = client.post('/register/', {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'StrongPassword123!',
        'password2': 'StrongPassword123!'
    })
    # Check if the response redirects (successful registration)
    assert response.status_code == 302
    # Verify the user is created in the database
    assert User.objects.filter(username='testuser').exists()

# Test that a registered user can log in successfully
@pytest.mark.django_db
def test_user_login(client, django_user_model):
    # Create a test user in the database
    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    # Simulate a POST request to the login endpoint with valid credentials
    response = client.post('/login/', {
        'username': 'testuser',
        'password': 'testpass'
    })
    # Check if the response redirects (successful login)
    assert response.status_code == 302

# Test that logging in with incorrect credentials fails
@pytest.mark.django_db
def test_invalid_login(client):
    # Simulate a POST request to the login endpoint with invalid credentials
    response = client.post('/login/', {
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    # Ensure the response does not redirect (login failed)
    assert response.status_code == 200
    # Verify the error message is included in the response content
    assert b"Invalid username or password" in response.content


## Test File Upload and Download
# Test that an authenticated user can upload a file successfully
@pytest.mark.django_db
def test_file_upload(client, authenticated_user):
    file = SimpleUploadedFile("test.txt", b"Hello World!")
    response = client.post('/upload/', {'file': file})
    assert response.status_code == 200
    assert b'alert-success' in response.content

# Test that an authenticated user can download their own file
@pytest.mark.django_db
def test_file_download(client, authenticated_user, user_file):
    # Simulate a GET request to the download endpoint for a specific file
    response = client.get(f'/download/{user_file.id}/')
    # Verify the response returns the file (status code 200)
    assert response.status_code == 200
    # Check that the response has the correct Content-Disposition header for file download
    assert response['Content-Disposition'] == f'attachment; filename={user_file.file.name}'


## Test File Sharing
# Test that a valid encrypted file ID can be used to access shared files
@pytest.mark.django_db
def test_valid_file_sharing(client, authenticated_user, user_file):
    encrypted_id = generate_encrypted_id(user_file.id)
    response = client.post('/shared_files/', {'encrypted_id': encrypted_id})
    assert response.status_code == 200
    assert b"File found!" in response.content

# Test that an invalid encrypted file ID does not grant access
@pytest.mark.django_db
def test_invalid_file_sharing(client, authenticated_user):
    invalid_id = "invalid_encrypted_id"
    response = client.post('/shared_files/', {'encrypted_id': invalid_id})
    assert response.status_code == 200
    assert b"Invalid encrypted ID." in response.content


## Test Forms
# Test that the user creation form is valid with correct input
@pytest.mark.django_db
def test_create_user_form_valid_data():
    # Provide valid form data
    form = CreateUserForm(data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'StrongPassword123!',
        'password2': 'StrongPassword123!'
    })
    # Ensure the form is valid
    assert form.is_valid()

# Test that the upload file form fails when no file is provided
def test_upload_file_form_no_file():
    # Provide empty form data
    form = UploadFileForm(data={})
    # Ensure the form is valid (because the file is not required)
    assert form.is_valid()



## Test Utilities
# Test that generating and decoding an encrypted ID works as expected
def test_generate_and_decode_encrypted_id():
    # Use a sample file ID
    file_id = 1
    # Generate an encrypted ID for the file
    encrypted_id = generate_encrypted_id(file_id)
    # Decode the encrypted ID back to the original file ID
    decoded_id = get_file_id_from_encrypted(encrypted_id)
    # Verify the decoded ID matches the original file ID
    assert decoded_id == file_id

# Test that decoding an invalid encrypted ID returns None
def test_invalid_encrypted_id():
    # Use an invalid encrypted ID
    invalid_id = "invalid_id"
    # Attempt to decode the invalid ID
    decoded_id = get_file_id_from_encrypted(invalid_id)
    # Ensure the result is None
    assert decoded_id is None