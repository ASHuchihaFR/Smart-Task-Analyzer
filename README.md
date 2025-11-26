# 📊 Smart Task Analyzer

**Internship Assignment Project**

A **full-stack Task Prioritization System** based on multi-factor decision scoring. Users can enter tasks in a React frontend, and the **Django REST API calculates priority scores** using urgency, importance, estimated effort, and dependency impact. The system ranks tasks and provides **priority-based recommendations**, making planning smarter and more efficient for individuals and teams.

---

## 🚀 Project Features

### 🔹 Frontend (React)

✔ Interactive UI to add tasks dynamically
✔ Input: Title, Due Date, Effort (hours), Importance (1–10)
✔ Live visual task display
✔ Button to analyze tasks via backend API
✔ “Backend API Connected” status indicator
✔ Real-time prioritized ranking display

---

### 🔹 Backend (Django REST API)

✔ `/api/prioritize/` endpoint accepts list of tasks
✔ Calculates priority score using **custom weighted scoring algorithm**
✔ Handles urgency, importance, effort, circular dependencies, and dependency impact
✔ Returns **sorted ranked list of tasks with priority score**
✔ Supports **balanced, high-impact, fastest-wins, and deadline-driven profiles**
✔ Includes **unit tests** for scoring logic

---

### 🧠 Scoring Algorithm

Each task is evaluated using four main factors:

| Factor              | Logic                                     |
| ------------------- | ----------------------------------------- |
| Urgency             | Earlier or overdue tasks get higher score |
| Importance          | User-rated importance (1–10)              |
| Effort              | Less effort → higher priority             |
| Dependency Impact   | Tasks blocking others get a boost         |
| Circular Dependency | If detected → penalty applied             |

Final Score:

```
Priority Score = 
(w_urgency × urgency) +
(w_importance × importance) +
(w_effort × effort) +
(w_dependencies × dependency_score)
```

Weight profiles:

| Profile         | Urgency | Importance | Effort | Dependencies |
| --------------- | ------- | ---------- | ------ | ------------ |
| Balanced        | 0.30    | 0.30       | 0.20   | 0.20         |
| High Impact     | 0.20    | 0.50       | 0.10   | 0.20         |
| Fastest Wins    | 0.15    | 0.15       | 0.50   | 0.20         |
| Deadline Driven | 0.60    | 0.20       | 0.10   | 0.10         |

---

## 🛠 Tech Stack

| Component             | Technology                     |
| --------------------- | ------------------------------ |
| Frontend              | React (JavaScript, HTML, CSS)  |
| Backend               | Django + Django REST Framework |
| Styling               | Tailwind / Basic CSS           |
| API Testing           | Postman                        |
| Unit Testing          | Django TestCase                |
| Dependency Management | `pip`, `requirements.txt`      |
| Version Control       | Git & GitHub                   |

---

## 📂 Project Structure

```
Smart Task Analyzer/
│── backend/
│   ├── tasks/
│   │   ├── views.py
│   │   ├── scoring.py
│   │   ├── tests.py
│   │   ├── urls.py
│   ├── manage.py
│   ├── requirements.txt
│   ├── settings.py
│
│── frontend/
│   ├── src/
│   │   ├── TaskAnalyzer.jsx
│   │   ├── App.js
│   │   ├── index.js
│   ├── package.json
│
│── README.md
│── .gitignore
```

---

# 🌐 API Usage Guide

### 🎯 Endpoint

```
POST http://127.0.0.1:8000/api/prioritize/
```

### ▶ Request Body

```json
[
  {
    "id": 1,
    "title": "Complete Assignment",
    "due_date": "2025-01-05",
    "estimated_hours": 3,
    "importance": 8,
    "dependencies": []
  },
  {
    "id": 2,
    "title": "Study for Exam",
    "due_date": "2024-12-10",
    "estimated_hours": 5,
    "importance": 9,
    "dependencies": []
  }
]
```

### ✔ Response Format

```json
[
  {
    "id": 2,
    "title": "Study for Exam",
    "priority_score": 92.5
  },
  {
    "id": 1,
    "title": "Complete Assignment",
    "priority_score": 75.3
  }
]
```

---

# ⚙ Installation and Setup

## 1️⃣ Backend Setup (Django)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at:
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 2️⃣ Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```

Frontend runs at:
👉 [http://localhost:3000/](http://localhost:3000/)

---

# 🧪 Unit Testing

File: `backend/tasks/tests.py`

Run tests:

```bash
cd backend
venv\Scripts\activate
python manage.py test
```

✔ Tests cover:

* Score calculation
* Overdue priority logic
* Circular dependency detection
* Profile-based scoring change

---

# 📦 GitHub Submission Requirements Checklist

| Requirement          | Status |
| -------------------- | ------ |
| Django backend code  | ✔      |
| React frontend code  | ✔      |
| requirements.txt     | ✔      |
| README.md            | ✔      |
| Minimum 3 unit tests | ✔      |
| Clean commit history | ✔      |

---

# 🌟 Future Enhancements

| Feature                   | Benefit                     |
| ------------------------- | --------------------------- |
| User Authentication       | Personal task storage       |
| Database Integration      | Save tasks permanently      |
| AI-based task suggestions | Smarter productivity        |
| Dashboard with charts     | Visual performance analysis |
| Mobile App version        | Anywhere productivity       |

---

# ✨ Final Notes

🔹 This project implements both **API-based backend logic and real-time frontend interaction**
🔹 Shows understanding of **algorithms, REST APIs, React UI, and Django backend**
🔹 Includes **unit testing, proper Git structure, and deployment readiness**

---

## 💡 Developed By

**Ashish Chauhan**



