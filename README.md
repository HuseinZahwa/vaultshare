# 🔒 VaultShare

**VaultShare** is a secure file-sharing application built with Django. It allows users to upload encrypted files, manage access permissions, and track file usage.

## 🚀 Features

- **🔐 Secure File Uploads** – All files are encrypted before storage.
- **👤 User Authentication** – Only registered users can upload and access files.
- **📊 Real-Time Access Tracking** – Monitor who accessed your files and when.
- **⚡ Lightweight & Fast** – Built with Django and SQLite.

## 🛠️ Technologies Used

- **Backend:** Django (Python)
- **Database:** SQLite
- **Security:** Django Authentication, Encrypted File Storage

- ## 📸 Screenshots

## VaultShare

A secure file-sharing application built with Django, featuring user authentication and encrypted file uploads.

### **Screenshots**

#### **Login Page**
![Login Page](images/LoginPage.png)

#### **Home Page**
![Home Page](images/HomePage.png)

#### **Upload a File**
![Upload a File](images/UploadAFile.png)

#### **Your Uploaded Files**
![Your Uploaded Files](images/YourUploadedFiles.png)

#### **Copy File ID**
![Copy File ID](images/CopyFileID.png)

#### **Shared Files**
![Shared Files](images/SharedFiles.png)

#### **Use a File ID**
![Use a File ID](images/UseAFileID.png)




## 📥 Installation Guide
```sh
1️⃣ Clone the Repository

git clone https://github.com/HuseinZahwa/vaultshare.git
cd vaultshare

2️⃣ Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Apply Migrations

python manage.py migrate

5️⃣ Create a Superuser (Optional)

python manage.py createsuperuser

6️⃣ Run the Development Server

python manage.py runserver

Now, open your browser and go to http://127.0.0.1:8000/ 🎉
