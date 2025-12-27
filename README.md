# 🧩AI Tool Finder - Backend Management and Review System

📝 AI Tool Finder is a backend-only application designed to help users explore, filter, and review various AI tools available in the industry. It acts as a centralized platform where users can easily discover AI tools based on their category, pricing model, and rating efficiency.

## 📚 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Architecture & Folder Structure](#-architecture--folder-structure)
5. [Database Schema (Models)](#-database-schema-models)
6. [API Endpoints Documentation](#-api-endpoints-documentation)
    - [User APIs](#user-apis)
    - [Review APIs](#review-apis)
    - [Admin APIs](#admin-apis)
7. [Filtering Logic](#-filtering-logic)
8. [Rating Calculation Logic](#-rating-calculation-logic)
9. [Setup & Installation Guide](#-setup--installation-guide)
10. [How to Run the Application](#-how-to-run-the-application)
11. [Testing Instructions (Pytest)](#-testing-instructions-pytest)
12. [Screenshots & Demo](#-screenshots--demo)
13. [Contributors](#-contributors)
14. [Future Enhancements](#-future-enhancements)

## 🏆 Project Overview

This system enables users to:
- View all AI tools stored in the database
- Apply multiple filters (like category, price type, rating) to find suitable AI tools
- Submit their own reviews and rate tools based on experience

To ensure data accuracy and prevent misuse, all user reviews must be approved by an Admin before they influence the tool’s final rating score. The admin has complete control over tool management and review moderation.

The project focuses purely on backend functionality such as:
✔ Clean REST API Design  
✔ Efficient Database Modeling  
✔ Automatic Rating Recalculation  
✔ Admin Moderation Workflow  
✔ Real-world Filtering Logic  

This backend can later be paired with any frontend or mobile interface for complete usage.

---

## 🚀 Features

### 🔹 User Functionalities
- Retrieve a complete list of AI tools
- Filter tools using multiple query parameters:
  - Category (e.g., NLP, Computer Vision)
  - Pricing Type (Free, Paid, Subscription)
  - Minimum Rating (e.g., >= 4 stars)
- Submit reviews including:
  - Rating (1–5 stars)
  - Optional comments

### 🔹 Admin Functionalities
- Add new AI tools into the platform
- Edit or update existing tools
- Delete any tool if required
- Approve or reject user-submitted reviews

### 🔹 Rating System
- Only *Approved* reviews contribute to a tool’s rating
- Rating gets automatically updated when new reviews are approved

### 🔹 Backend Architecture
- Separate routes for users and admins
- Efficient business logic handling
- Database-driven review aggregation

---

## 🛠 Tech Stack

| Stack Component | Technology Used |
|----------------|----------------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Database | SQLite3 |
| Testing | Pytest |
| Server | Uvicorn |


## 📂 Architecture & Folder Structure

ai-tools-backend/
│
├── app/
│   ├── admin/
│   │   └── routes.py        # Admin-only routes (secure: add/edit/delete tools, review moderation)
│   │
│   ├── user/
│   │   └── routes.py        # Public endpoints (list tools, submit reviews)
│   │
│   ├── models.py            # SQLAlchemy DB models (Tool, Review, Admin)
│   ├── schemas.py           # Pydantic models for validation & serialization
│   ├── crud.py              # Business logic and DB operations
│   ├── auth.py              # JWT Authentication, admin verification
│   ├── database.py          # DB engine, session config
│   ├── main.py              # FastAPI app startup, routing & DB initialization
│   ├── seed_admin.py        # Script to seed or update admin credentials
│
├── test.py                  # Automated API test script (Pytest/TestClient)
├── run.py                   # Main server run script using Uvicorn
├── README.md                # Full documentation (this file)
└── requirements.txt         # Dependencies (to be added if not present)


## 🧱 Database Schema (Models)

The backend uses **SQLAlchemy ORM** and SQLite with three major tables:

---

### 🔹 AITool Table

| Column         | Type       | Constraints       |Description                                     |
|----------------|------------|------------------|--------------------------------------------------|
| id             | String     | Primary Key       | UUID for each tool                               |
| name           | String     | Required          | Tool name                                        |
| use_case       | String     | Optional          | Tool's purpose (ex: Summarization)               |
| category       | String     | Optional          | Category (NLP, CV, Dev Tools, Productivity)      |
| pricing_type   | String     | Required          | Free / Paid / Subscription                        |
| average_rating | Float      | Default: 0.0      | Computed only from **approved** reviews          |

🧩 Relationship  
`AITool` ➝ `Review` (One-to-Many)

---

### 🔹 Review Table

| Column     | Type       | Constraints       | Description                                     |
|-----------|------------|------------------|-------------------------------------------------|
| id        | String     | Primary Key       | Unique review ID                                |
| tool_id   | String     | Foreign Key       | References AITool.id                             |
| rating    | Integer    | Required (1–5)    | Rating given by user                            |
| comment   | String     | Optional          | User feedback                                   |
| status    | String     | Default: Pending  | Pending / Approved / Rejected (for moderation)  |
| created_at| DateTime   | Auto timestamp    | When the review was submitted                   |

📝 **Only Approved reviews** affect rating calculation

---

### 🔹 Admin Table

| Column          | Type       | Constraints  | Description                     |
|----------------|------------|--------------|---------------------------------|
| username       | String     | Primary Key  | Unique admin login ID           |
| hashed_password| String     | Required     | Secure bcrypt hashed password   |

---


## 🔌 API Endpoints Documentation

### 👤 User APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/tools` | Fetch tools with filters |

Filters Supported →  
`category`, `pricing_type`, `rating>=value`

---

### ⭐ Review APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/review` | Submit a review |

➡ Status becomes **Pending** until admin approval

---

### 🛡 Admin APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/login` | Login & get token |
| POST | `/admin/tools` | Add tool |
| PUT | `/admin/tools/{tool_id}` | Edit tool |
| DELETE | `/admin/tools/{tool_id}` | Delete tool |
| GET | `/admin/reviews` | Get reviews by status |
| PATCH | `/admin/reviews/{review_id}/approve` | Approve review & update rating |
| PATCH | `/admin/reviews/{review_id}/reject` | Reject review |


## 🔍 Filtering Logic

The user tools listing API supports advanced multi-filter queries:


### ✔ Filter Parameters Supported
| Query Param | Example | Description |
|------------|---------|-------------|
| `category` | NLP | Filters tools by use-case category |
| `pricing_type` | Free | Matches cost type Free / Paid / Subscription |
| `rating` | 4 | Returns tools with **average rating ≥ value** |

📌 All filters must be satisfied (**AND condition**)

## ⭐ Rating Calculation Logic

User reviews directly influence a tool’s average rating — but only after admin moderation.

### 🔐 Moderation Based Rating System
When a user submits a review:
- It is first stored with **status = "Pending"**
- Only an **Admin** can approve or reject the review

🔁 Once a review is **approved**:
1. Review status becomes `"Approved"`
2. Backend calculates average rating:
3. Result is updated into `AITool.average_rating`
4. The updated rating is shown in public GET `/users/tools`

---

### ⚠️ Important Rules

| Case | Will it update the rating? | Reason |
|------|----------------------------|--------|
| Approved review | ✔ Yes | It reflects valid feedback |
| Pending review | ❌ No | Awaiting admin decision |
| Rejected review | ❌ No | Marked as invalid feedback |

---

### 🔁 Example Rating Update Flow

| Step | Action | Rating Effect |
|------|--------|---------------|
| 1️⃣ User submits review (rating = 5) | Status = Pending | No update |
| 2️⃣ Admin approves the review | Status = Approved | New average calculated |
| 3️⃣ Another review approved (rating = 4) | Updated | New average = (5+4)/2 = 4.5 |

---



### 🎯 Why This Project?
This system simulates a real-world backend workflow found in top product marketplaces, helping developers learn:
- API structure design
- Secure content moderation
- Data validation & consistency
- Rating aggregation using computed fields


