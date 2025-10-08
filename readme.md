# 🏥 Healthcare Management API (Django + PostgreSQL)

A backend system built using **Django REST Framework** and **PostgreSQL** to manage **Patients**, **Doctors**, and their mappings.  
The project includes **JWT Authentication** to secure APIs and enforce access control (patients can manage only their own data).

---

## 📖 Overview

This project provides a simple but scalable backend for healthcare management. It allows:
- 👩‍⚕️ Patients to register/login and manage their own health records.  
- 🧑‍⚕️ Doctors to be listed and associated with patients.  
- 🔗 Mapping between patients and doctors for consultation tracking.  
- 🔐 JWT authentication for secure access.  

---

## ⚙️ Tech Stack

- **Backend Framework**: Django 5.x  
- **API Framework**: Django REST Framework (DRF)  
- **Database**: PostgreSQL  
- **Authentication**: JWT (using `djangorestframework-simplejwt`)  
- **Environment Management**: Python `venv`  
- **Deployment Ready**: Configurable via environment variables  

---

## 📂 Project Structure
```bash
healthcare_project/
│── core/ # Main Django app (models, views, serializers, permissions, urls)
│── healthcare_project/ # Project settings and configurations
│── manage.py # Django CLI entrypoint
│── requirements.txt # Project dependencies
│── .env.example # Example environment variables
│── README.md # Project documentation
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
    git clone https://github.com/your-username/healthcare-api.git
    cd healthcare-api
```
### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
    python -m venv venv
    source venv/bin/activate   # For Linux/Mac
    venv\Scripts\activate      # For Windows
    pip install -r requirements.txt
```
### 3️⃣ Configure Environment Variables

--- Create a .env file in the project root:

    DEBUG=True
    SECRET_KEY=your_secret_key

    # PostgreSQL Database
    DB_NAME=healthcare_db
    DB_USER=healthcare_db_user
    DB_PASSWORD=yourpassword
    DB_HOST=localhost
    DB_PORT=5432

    # JWT Config
    ACCESS_TOKEN_LIFETIME_MIN=60
    REFRESH_TOKEN_LIFETIME_DAYS=7

### 4️⃣ Run Migrations
```bash 
     python manage.py migrate
```
### 5️⃣ Create Superuser
```bash 
    python manage.py createsuperuser
```
### 6️⃣ Run the Server
```bash 
    python manage.py runserver
```
---Server available at: http://127.0.0.1:8000/

---

## 🔑 Authentication Flow (JWT)

### 1.Register a new user

    POST /api/auth/register/
    {
    "username": "avinash",
    "password": "mypassword",
    "email": "avinash@example.com"
    }

### 2.Login to get tokens
   
    POST /api/auth/login/
    {
    "username": "avinash",
    "password": "mypassword"
    }
--
     Response:
    {
        "refresh": "<your_refresh_token>",
        "access": "<your_access_token>"
    }

### 3.Use Access Token in requests
    Authorization: Bearer <your_access_token>

### 4.Refresh Token
    POST /api/auth/refresh/
    {
    "refresh": "<your_refresh_token>"
    }

---

## 📡 API Endpoints

### Patients

   - GET /api/patients/ → List patients (only logged-in user's records)
   - POST /api/patients/ → Create patient profile
   - PUT /api/patients/<id>/ → Update patient profile
   - DELETE /api/patients/<id>/ → Delete patient

### Doctors

   - GET /api/doctors/ → List all doctors (public)
   - POST /api/doctors/ → Create new doctor (auth required)
   - PUT /api/doctors/<id>/ → Update doctor info
   - DELETE /api/doctors/<id>/ → Delete doctor

### Patient-Doctor Mappings

   - GET /api/mappings/ → List all patient-doctor mappings
   - GET /api/mappings/patient/<patient_id>/ → Get all doctors for a patient
   - POST /api/mappings/ → Assign doctor to patient
   - DELETE /api/mappings/<id>/ → Remove mapping

---


## 🗄️ Database Schema (ERD)

    erDiagram
        USER {
            int id PK
            string username
            string password
            string email
        }

        PATIENT {
            int id PK
            string name
            int age
            string gender
            int user_id FK
        }

        DOCTOR {
            int id PK
            string name
            string specialization
        }

        PATIENT_DOCTOR {
            int id PK
            int patient_id FK
            int doctor_id FK
        }

        USER ||--o{ PATIENT : "owns"
        PATIENT ||--o{ PATIENT_DOCTOR : "maps to"
        DOCTOR ||--o{ PATIENT_DOCTOR : "maps to"

---

## 🧪 Example Usage (Postman)

    1.Register a user → get token

    2.Login → copy the access token

    3.In Postman → go to Authorization → Bearer Token → paste token

    4.Call /api/patients/ → you’ll only see your own patient profile

---

## 👨‍💻 Author

 Avinash Satalkar
 linkedin - https://www.linkedin.com/in/avinash-satalkar-10a934230/
