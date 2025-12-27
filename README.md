# 🤖 AI Tool Finder – Backend API

AI Tool Finder is a **backend-only REST API** built with **FastAPI ⚡** that helps users discover, filter, and review AI tools.  
Admins manage tools and moderate reviews to ensure accurate ratings ⭐.

---

## ✨ Features

### 👤 User
- 📋 View all AI tools
- 🔍 Filter tools by:
  - 🧠 Category
  - 💰 Pricing type
  - ⭐ Minimum rating
- ✍️ Submit reviews with rating & comments

### 🛡️ Admin
- 🔐 Secure admin login (JWT)
- ➕ Add new AI tools
- ✏️ Update existing tools
- 🗑️ Delete tools
- ✅ Approve / ❌ Reject user reviews

---

## 🛠️ Tech Stack

- 🐍 **Python**
- ⚡ **FastAPI**
- 🗄️ **SQLite + SQLAlchemy**
- 🔑 **JWT Authentication**
- 🧪 **Pytest**
- 🚀 **Uvicorn**

---


---

## 🔌 API Endpoints

### 👤 User APIs
- `GET /users/tools` 🔍 Get tools with filters
- `POST /users/review` ✍️ Submit a review

### 🛡️ Admin APIs
- `POST /admin/login` 🔐 Admin login
- `POST /admin/tools` ➕ Add tool
- `PUT /admin/tools/{id}` ✏️ Update tool
- `DELETE /admin/tools/{id}` 🗑️ Delete tool
- `PATCH /admin/reviews/{id}/approve` ✅ Approve review
- `PATCH /admin/reviews/{id}/reject` ❌ Reject review

---

## ⭐ Rating Logic

- 🕒 New reviews are created as **Pending**
- 🛡️ Admin approval is required
- ⭐ Only **Approved** reviews affect the average rating
- 🔄 Ratings update automatically after approval

---

## ⚙️ Setup & Run

```

pip install -r requirements.txt

python .\run.py

```


## 🧪 Testing

```
pytest test.py

```
