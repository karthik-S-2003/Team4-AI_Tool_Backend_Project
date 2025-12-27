# AI Tool Finder – Backend API

AI Tool Finder is a **backend-only REST API** built with FastAPI to manage and review AI tools.  
It allows users to browse AI tools and submit reviews, while admins control tool management and review approvals.

---

## Features

### User
- View list of AI tools
- Filter tools by:
  - Category
  - Pricing type
  - Minimum rating
- Submit reviews with rating and comments

### Admin
- Admin login (JWT authentication)
- Add, update, and delete AI tools
- Approve or reject user reviews
- Only approved reviews affect ratings

---

## Tech Stack

- Python
- FastAPI
- SQLite (SQLAlchemy ORM)
- JWT Authentication
- Pytest
- Uvicorn

---

## Project Structure

ai-tools-backend/
├── app/
│ ├── admin/ # Admin routes
│ ├── user/ # User routes
│ ├── models.py # Database models
│ ├── schemas.py # Request/response schemas
│ ├── crud.py # Business logic
│ ├── auth.py # Authentication
│ ├── database.py # Database setup
│ └── main.py # App entry point
├── test.py # Tests
├── run.py # Server runner
└── README.md



---

## API Endpoints

### User
- `GET /users/tools` – Get tools with filters
- `POST /users/review` – Submit a review

### Admin
- `POST /admin/login` – Admin login
- `POST /admin/tools` – Add tool
- `PUT /admin/tools/{id}` – Update tool
- `DELETE /admin/tools/{id}` – Delete tool
- `PATCH /admin/reviews/{id}/approve` – Approve review
- `PATCH /admin/reviews/{id}/reject` – Reject review

---

## Rating Logic

- Reviews are created with **Pending** status
- Only **Approved** reviews are used to calculate average rating
- Rating updates automatically after approval

---

## Setup & Run

```
pip install -r requirements.txt
python .\run.py

uvicorn app.main:app --reload

```


API Docs available at:

http://localhost:8000/docs


## Testing

```
pytest test.py

```
