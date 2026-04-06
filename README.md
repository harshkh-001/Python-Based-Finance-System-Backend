# Python-Based-Finance-System-Backend

## 📌 Overview

This project is a Python-based Finance Tracking Backend System built using Django. It allows users to manage financial transactions, analyze data, and interact with the system based on role-based access control.

The system is designed with a focus on:

- Clean backend architecture
- Proper API design
- Data handling & analytics
- Maintainability and scalability

## 🎯 Objective

The goal of this project is to demonstrate:

- Strong Python backend development skills
- Clean application design
- Proper API handling and validation
- Logical financial data processing
- Robust error handling

## 🏗️ Project Structure
```
finance_system/
│
├── Accounts/ # Authentication & user management
│ ├── login/logout/signup
│ └── custom user model
│
├── Api/ # All REST API endpoints
│ ├── transactions APIs
│ ├── analytics APIs
│ └── filtering APIs
│
├── Users/ # Frontend views (Django templates)
│ ├── dashboard
│ ├── role-based pages
│ └── UI logic
│
├── finance_system/ # Main project configuration
│ ├── settings.py
│ └── urls.py
│
└── manage.py
```


## 🚀 Features

### 1. 💰 Financial Records Management
- Create transactions (income/expense)
- View transactions
- Update transactions
- Delete transactions
- Filter transactions by:
  - Date
  - Category
  - Type

### 2. 📈 Financial Analytics
- Total Income
- Total Expenses
- Current Balance
- Category-wise breakdown
- Monthly summaries
- Recent activity tracking

### 3. 👥 Role-Based Access Control

| Role     | Permissions                                    |
|----------|------------------------------------------------|
| Admin    | Full access (CRUD + user management)          |
| Analyst  | View + filter + analytics                      |
| Viewer   | Read-only access                               |

### 4. 🔌 API Endpoints

#### 🔹 User APIs
- `GET /api/get_users/`

#### 🔹 Transaction APIs
- `GET /api/get_transactions/`
- `POST /create_transaction/`
- `POST /update_transaction/`
- `POST /delete_transaction/`

#### 🔹 Analytics APIs
- `GET /api/financial_summary/`
- `GET /api/category_breakdown/`
- `GET /api/monthly_summary/`
- `GET /api/recent_activity/`

#### 🔹 Filtering
- `GET /api/filter_transactions/?date=&category=&transaction_type=`

## 🛠️ Tech Stack

| Component          | Technology              |
|--------------------|-------------------------|
| Backend Framework  | Django                  |
| API Framework      | Django REST Framework   |
| Database           | SQLite (default)        |
| Language           | Python                  |

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone <your-repo-link>
cd finance_system
```

2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run Server
```bash
python manage.py runserver
```

## API Documentation

Swagger UI: http://127.0.0.1:8000/swagger/  
Redoc: http://127.0.0.1:8000/redoc/


## 🔐 Authentication Flow
Users login via /login

Sessions are maintained using Django authentication

Role is used for authorization across APIs and views

## ⚠️ Validation & Error Handling
### The system includes:

Input validation for forms and APIs

Proper HTTP status codes:

400 → Bad Request

401 → Unauthorized

403 → Forbidden

404 → Not Found

500 → Server Error

Safe database queries

Graceful failure handling

## 🧠 Design Decisions
Decision	Reason
Separation of Concerns	Accounts → Authentication, Api → Business logic, Users → UI
Role-Based Control	Simplified but effective RBAC system
Django ORM	Clean and efficient database operations
Modular Structure	Easy to scale and maintain
### 📊 Assumptions
Users are pre-assigned roles (admin, analyst, viewer)

Authentication is session-based (not JWT)

SQLite is sufficient for this scope

created_at is used for date-based operations

### 🧪 Testing the System
You can test:

APIs using Postman / browser

UI via Django templates

Role restrictions by logging in with different users

## 📌 Evaluation Mapping
Criteria	Implementation
Python Proficiency	Clean Django + DRF usage
Application Design	Modular apps (Accounts, Api, Users)
Functionality	Full CRUD + analytics
Logical Thinking	Financial summaries & filtering
Data Handling	ORM queries + aggregation
Validation	Input checks + error handling
Code Quality	Structured, readable code
Documentation	This README

## 📎 Future Improvements
- JWT Authentication
- Pagination for APIs
- Advanced analytics (charts, trends)
- Docker deployment
- PostgreSQL integration

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author
Harsh Khandelwal
