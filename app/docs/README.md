# 🧩 User Management Microservice (FastAPI + SQLite)

A modular, feature-based **User Management Microservice** built with **FastAPI**, providing authentication, authorization, signup, and JWT token support.

---

## 🚀 Features

- ✅ User Signup & Authentication  
- ✅ JWT-based Authorization  
- ✅ Password Hashing (bcrypt)  
- ✅ SQLite Database Support  
- ✅ Modular Folder Structure  
- ✅ FastAPI Interactive Docs (`/docs`)

---

## 🏗️ Project Structure

user_management/
│
├── api/
│ └── auth/
│ └── v1.py
│
├── core/
│ ├── config.py
│ └── database/
│ ├── base.py
│ └── session.py
│
├── services/
│ └── auth/
│ ├── jwt/
│ │ ├── routes.py
│ │ ├── schemas.py
│ │ └── service.py
│ ├── models.py
│ ├── schemas.py
│ └── service.py
│
├── requirements/
│ ├── requirements.txt
│ └── requirements-dev.txt
│
├── docs/
│ └── README.md
│
└── main.py