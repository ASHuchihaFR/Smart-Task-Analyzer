# 🚀 Smart Task Analyzer

A Django-based API and React frontend system that intelligently prioritizes tasks using urgency, importance, effort, and dependency analysis.

---

## 📦 Setup Instructions

### 🔧 Backend (Django API)

1. Navigate to backend folder:

   ```bash
   cd backend
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run Django server:

   ```bash
   python manage.py runserver
   ```

Backend will run at 👉 `http://127.0.0.1:8000/`

---

### 🎨 Frontend (React)

1. Open a new terminal and navigate to frontend folder:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Start frontend:

   ```bash
   npm start
   ```

Frontend runs at 👉 `http://localhost:3000/`

---

## 🧠 Algorithm Explanation (Priority Scoring)

The priority scoring algorithm analyzes tasks based on **four major factors**:
**Urgency**, **Importance**, **Effort**, and **Dependencies**. It assigns a score between **0 and 100** for each task.

### 1️⃣ Urgency (How soon is the deadline?)

Tasks with nearer or overdue deadlines are assigned higher priority.

* If the task is **overdue**, it receives a strong penalty boost.
* If due soon, its priority gradually increases.

**Formula:**

> If overdue → `1 + abs(days overdue) × 0.15`
> If upcoming → `1 / (1 + days remaining)`

---

### 2️⃣ Importance (How valuable is the task?)

Importance is rated from **1 to 10** by the user.
It is normalized: `importance / 10`.

---

### 3️⃣ Effort (How long will it take?)

Tasks requiring fewer estimated hours are prioritized.

> Formula: `1 - min(hours / 40, 1)`

---

### 4️⃣ Dependencies (Does this task block others?)

If a task is required to complete other tasks, its priority increases.
However, **circular dependencies** receive a 0 score.

---

### 🧮 Total Score Calculation

```python
score = (urgency * weight_urgency) +
        (importance * weight_importance) +
        (effort * weight_effort) +
        (dependencies * weight_dependencies)
```

Each scoring factor is then multiplied by 100 and sorted in descending order.

This makes the system **dynamic**, **scalable**, and suitable for real-time task planning.

---

## ⚙️ Design Decisions & Trade-offs

| Decision                         | Reason                                         |
| -------------------------------- | ---------------------------------------------- |
| Used Django REST Framework       | Quick API development, easy JSON handling      |
| React for Frontend               | Live task updates & better user interaction    |
| Chose JSON for API communication | Lightweight, frontend-friendly                 |
| Used local fallback scoring      | Ensures frontend still works without backend   |
| Simplified weight profiles       | Enough for initial MVP, but scalable later     |
| No database storage              | Requirement focused on processing, not storage |

---

## ⏱ Time Breakdown

| Task                                    | Time Spent     |
| --------------------------------------- | -------------- |
| Understanding PDF requirements          | 2 hours        |
| Backend API development & scoring logic | 4.5 hours      |
| Frontend UI with React and Tailwind     | 4 hours        |
| API integration & bug fixing            | 2 hours        |
| Writing unit tests                      | 1 hour         |
| Git + README documentation              | 1 hour         |
| Total                                   | **14.5 hours** |

---

## 🧪 Unit Tests Implemented

✔ Score is always between 0 and 100
✔ Overdue tasks receive higher priority
✔ Circular dependencies receive penalty
✔ High importance tasks get prioritized in high-impact mode

---

## 🚀 Future Improvements

🔹 Add user login and database storage
🔹 Enable task editing and deletion
🔹 Add Gantt-style task scheduling
🔹 Export priority results as PDF/Excel
🔹 Implement drag-and-drop task sorting

## 💡 Developed By
Ashish Chauhan
chauhan.ashish250204@gmail.com
