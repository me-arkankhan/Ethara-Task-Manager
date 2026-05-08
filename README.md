# Ethara.AI - Workspace Task Manager 🚀

A modern, fast, and secure role-based task management portal built with Flask. Designed for serious teams to ship serious work without the noise. 

## 🌐 Live Demo
**Play with the live app here:  https://web-production-dbdeb.up.railway.app/login **

---

## ✨ Key Features
* **Role-Based Access Control (RBAC):** * **Admins** can assign tasks, view team analytics, and manage the workspace.
  * **Members** have a clean interface to view and complete their assigned tasks.
* **Asynchronous Operations:** Task creation, deletion, and completion use the Fetch API for a seamless, no-reload experience.
* **Premium UI/UX:** A custom dark mode (Aurora Theme) with glassmorphism panels, 3D interactive buttons, and a sleek video-style loading screen.
* **Fully Responsive:** Optimized for both desktop and mobile screens with an interactive hamburger menu.
* **Secure:** Passwords are fully hashed and salted using `Werkzeug` security before entering the database.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Bootstrap 5 (for grid layout)
* **Deployment:** Railway (Gunicorn WSGI)

---

## ⚙️ Local Setup Instructions

If you want to run this project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/me-arkankhan Ethara-Task-Manager.git]