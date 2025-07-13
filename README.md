

---

## 📘 `README.md` for TIL Journal App

```markdown
# 📓 Today I Learned (TIL) Journal App

A minimal and secure full-stack journal application that allows users to log what they learn each day. Built with FastAPI, MongoDB, and JWT authentication.

---

## 🚀 Features

- ✅ User registration and login with secure JWT auth
- 🛡️ Token refresh & logout
- ✍️ Create, view, update, and delete personal TIL journal entries
- 🔍 Search/filter entries by keywords or tags
- 📅 Timestamped entries with auto-tracking
- 🔐 Private, user-specific entries (no public feed)
- 🌍 RESTful API backend with FastAPI
- 📦 MongoDB as the document database

---

## 🧱 Tech Stack

| Layer       | Technology     |
|-------------|----------------|
| Backend     | FastAPI (Python) |
| Database    | MongoDB (Motor) |
| Auth        | JWT + OAuth2 password flow |
| Frontend    | (Planned) React or other SPA framework |
| Deployment  | (Planned) Docker / Railway / Render |

---

## 🏗️ Project Structure

```

app/
├── main.py
├── models/
│   └── User.py, Journal.py
├── routers/
│   └── users.py, entries.py
├── schema/
├── services/
├── config/
├── utils/
└── .env

````

---

## 🔧 Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/TID_Journal.git
   cd TID_Journal
````

2. **Create a virtual environment:**

   ```bash
   python -m venv .env
   source .env/bin/activate  # or `.env\Scripts\activate` on Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   Create a `.env` file with:

   ```env
   MONGO_URI=mongodb://localhost:27017
   JWT_SECRET_KEY=your_super_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run the app:**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🔐 API Authentication

All journal routes are protected and require a valid **access token** in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

---

## 📬 API Endpoints (sample)

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| POST   | /auth/register | Register a new user      |
| POST   | /auth/login    | Get JWT access + refresh |
| POST   | /auth/refresh  | Refresh access token     |
| POST   | /auth/logout   | Invalidate refresh token |
| POST   | /entries/      | Create new TIL entry     |
| GET    | /entries/      | List all user entries    |
| PUT    | /entries/{id}  | Update a journal entry   |
| DELETE | /entries/{id}  | Delete a journal entry   |

---

## 📌 Future Plans

* Add frontend (React, Next.js, or Svelte)
* Markdown support for entries
* Tag filtering & search
* Export to PDF or Markdown
* Mobile-friendly interface

---

## 🧑‍💻 Author

**Abdirashid Abubakar**
[GitHub Profile](https://github.com/YOUR_USERNAME)

---

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

```
```
