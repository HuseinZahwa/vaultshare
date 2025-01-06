import os
import pytest
import shutil
import tempfile
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


# Override MEDIA_ROOT for tests to store test files in a temporary directory
@pytest.fixture(autouse=True)
def override_media_root(settings):
    settings.MEDIA_ROOT = tempfile.mkdtemp()


# Clean up MEDIA_ROOT after tests to prevent clutter
@pytest.fixture(autouse=True)
def clean_media_root():
    yield  # Yield to allow tests to run
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


# Create and authenticate a test user
@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    return user


# Create a test file associated with the authenticated user
@pytest.fixture
def user_file(authenticated_user):
    from file_manager.models import UserFile
    test_file = SimpleUploadedFile("test.txt", b"Sample content")
    user_file = UserFile.objects.create(user=authenticated_user, file=test_file)
    return user_file
