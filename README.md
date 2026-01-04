# 🤖 AI Tool Finder – Full Stack Application

AI Tool Finder is a full-stack web application that allows users to discover, filter, and review AI tools, while administrators manage tools and moderate reviews.

The project is built with a FastAPI backend and a vanilla HTML/CSS/JavaScript frontend, following a clean client–server architecture.

# 🌟 Key Features
  - 👤 User

  - 📋 Browse all AI tools

  - 🔍 Search tools by name

  - 🧠 Filter by category

  - 💰 Filter by pricing type

  - ⭐ Sort tools by rating

  - ✍️ Submit reviews with star rating & comments

  - ⏳ Reviews require admin approval

  - 🛡️ Admin

  - 🔐 Secure admin login (JWT authentication)

  - ➕ Add new AI tools

  - 🗑️ Delete existing tools

  - 📊 View all tools with ratings

  - ✅ Approve reviews

  - ❌ Reject reviews

# 🛠️ Tech Stack

## Frontend

  - 🧱 HTML5

  - 🎨 CSS3 (custom styling, Flexbox, Grid)

  - ⚙️ Vanilla JavaScript

  - 🎯 Font Awesome Icons

## Backend

  - 🐍 Python

  - ⚡ FastAPI

  - 🗄️ SQLite + SQLAlchemy ORM

  - 🔑 JWT Authentication

  - 🚀 Uvicorn

  - 🧪 Pytest

# 📁 Project Folder Structure

```

Team4-AI_Tool_Backend_Project-js/
│
├── app/                      # Backend source code
│   ├── admin/
│   │   └── routes.py         # Admin APIs
│   ├── user/
│   │   └── routes.py         # User APIs
│   ├── crud.py               # Database operations
│   ├── main.py               # FastAPI app entry
│
├── frontend/                 # Frontend (Static files)
│   ├── index.html            # User UI
│   ├── index.css             # User styles
│   ├── script.js             # User logic
│   ├── admin.html            # Admin UI
│   ├── admin.css             # Admin styles
│   ├── admin.js              # Admin logic
│   └── style.css             # Shared styles
│
├── ai_tools.db               # SQLite database
├── requirements.txt          # Python dependencies
├── run.py                    # Run backend server
├── test.py                   # Backend tests
├── README.md                 # Project documentation
└── .gitignore

```


# 🧭 System Architecture & Flow

```

Browser (Frontend)
   |
   |  HTTP Requests (fetch API)
   v
FastAPI Backend
   |
   |  CRUD Operations
   v
SQLite Database

```

# 🔄 Flow Explanation

  - User/Admin interacts with the frontend UI

  - Frontend sends API requests using fetch()

  - FastAPI processes requests & business logic

  - Database stores and retrieves data

  - Response sent back to frontend and rendered

# 🔌 API Endpoints

## 👤 User APIs

  - GET /users/tools – Get all tools (with filters)

  - GET /users/reviews – Get approved reviews

  - POST /users/review – Submit a review

## 🛡️ Admin APIs

  - POST /admin/login – Admin login

  - POST /admin/tools – Add new tool

  - DELETE /admin/tools/{id} – Delete tool

  - PATCH /admin/reviews/{id}/approve – Approve review

  - PATCH /admin/reviews/{id}/reject – Reject review

## ⭐ Review & Rating Logic

  - 🕒 New reviews are stored as Pending

  - 🛡️ Admin must approve reviews

  - ⭐ Only Approved reviews affect average rating

  - 🔄 Ratings recalculate automatically after approval

# ⚙️ Setup & Run Project


1️⃣ Install dependencies

```

pip install -r requirements.txt

```

2️⃣ Run backend server

```

python run.py

```

Backend runs at:

```

http://127.0.0.1:9000

```

3️⃣ Run frontend

```

Open frontend/index.html using:

VS Code Live Server OR

Directly open in browser

```

# 🧪 Testing

```

pytest test.py

```

# ✅ Project Status

✔ Backend APIs complete

✔ Frontend UI implemented

✔ Admin panel functional

✔ JWT authentication working

✔ Ready for submission / demo

# 👥 Team Collaboration Notes

Always run git pull origin main before starting work

Frontend and backend are maintained in the same repository

Avoid force pushes on main