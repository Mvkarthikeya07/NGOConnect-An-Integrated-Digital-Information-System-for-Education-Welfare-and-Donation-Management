<div align="center">

<img src="https://img.shields.io/badge/NGOConnect-v1.0.0-2ea44f?style=for-the-badge" alt="Version">
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
<img src="https://img.shields.io/badge/Status-Academic%20Prototype-orange?style=for-the-badge" alt="Status">

<br/><br/>

# 🌐 NGOConnect An Integrated Digital Information System for Education Welfare and Donation Management

### An Integrated Digital Information System for Education, Welfare, and Donation Management

> *Digitally transforming the operational backbone of Non-Governmental Organizations — one record at a time.*

<br/>

[Features](#-features) · [Tech Stack](#-tech-stack) · [Project Structure](#-project-structure) · [Getting Started](#-getting-started) · [Screenshots](#-screenshots) · [Database Schema](#-database-schema) · [Roadmap](#-roadmap) · [License](#-license)

<br/>

</div>

---

## 📌 Overview

**NGOConnect** is a full-stack, web-based information system purpose-built to digitize and centralize the core administrative operations of Non-Governmental Organizations. It replaces fragmented spreadsheets and paper-based record keeping with a unified, responsive, and maintainable platform.

Built as part of the **Software Engineering and Project Management (SEPM)** curriculum, NGOConnect demonstrates end-to-end system design — from requirements analysis and data modeling to UI development and backend implementation — all while addressing genuine challenges faced by real-world NGOs.

The system manages three critical domains:

| Domain | What it solves |
|---|---|
| 🎓 **Beneficiary Management** | Tracks individuals receiving education, health, and welfare support |
| 🤝 **Volunteer Management** | Maintains volunteer profiles, roles, and contact details |
| 💰 **Donation Management** | Records donor contributions, amounts, and designated purposes |

---

## ✨ Features

### 🔐 Authentication
- Admin login with client-side credential validation via `localStorage`
- Password reset workflow (update & persist new password in-browser)
- Designed for future upgrade to server-side hashed authentication

### 📊 Live Dashboard
- Real-time aggregate statistics: total beneficiaries, volunteers, and cumulative donations
- Card-based summary UI for instant situational awareness
- All metrics computed dynamically via SQL aggregation on every page load

### 👨‍🎓 Beneficiary Management
- Add new beneficiaries with name, age, education level, and support category
- View the complete beneficiary registry in a structured table
- One-click record deletion via dedicated route

### 🤝 Volunteer Management
- Register volunteers with name, assigned role, and contact information
- Full roster view with inline delete capability
- Supports structured coordination across volunteer teams

### 💰 Donation Management
- Log donations with donor name, contribution amount, and purpose
- Tabular donation history with deletion support
- Dashboard dynamically reflects cumulative donation totals via `SUM()` aggregation

### 🎨 UI & Navigation
- Persistent sidebar navigation across all authenticated pages
- Responsive, application-style layout using custom CSS
- Consistent design language: topbar, card grid, form panels, and data tables
- Clean separation of layout (`base.html`) from page-specific content via Jinja2 template inheritance

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript | Structure, styling, client-side logic |
| **Backend** | Python 3, Flask | Routing, request handling, template rendering |
| **Database** | SQLite (`ngo.db`) | Persistent storage via lightweight file-based RDBMS |
| **Templating** | Jinja2 (via Flask) | Server-side HTML rendering with data injection |
| **Auth** | JavaScript + `localStorage` | Prototype-level credential management |
| **Styling** | Custom CSS (`dashboard.css`) | Dashboard layout, sidebar, forms, cards |

---

## 📁 Project Structure

```
NGOConnect/
│
├── app.py                  # Flask application — all routes and controller logic
├── database.py             # DB connection factory + schema initialization
├── ngo.db                  # SQLite database file (auto-created on first run)
├── requirements.txt        # Python dependencies (flask)
│
├── templates/
│   ├── base.html           # Master layout — sidebar, topbar, content slot
│   ├── login.html          # Login & password reset page (standalone, no base)
│   ├── dashboard.html      # Live metrics overview
│   ├── beneficiaries.html  # Beneficiary CRUD interface
│   ├── volunteers.html     # Volunteer CRUD interface
│   └── donations.html      # Donation CRUD interface
│
└── static/
    └── css/
        └── dashboard.css   # All application styles
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- `pip` package manager

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/NGOConnect.git
cd NGOConnect

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the development server
python app.py
```

> The application will be available at **http://127.0.0.1:5000**

### Default Login Credentials

| Field | Value |
|---|---|
| **Username** | `admin` *(pre-filled, read-only)* |
| **Password** | `admin123` |

> ⚠️ Authentication is client-side only (prototype). Credentials are stored in `localStorage`. Do **not** deploy this as-is in a production environment.

---

## 🗄 Database Schema

Three tables are auto-created on application startup via `database.py`:

```sql
-- Individuals receiving NGO support
CREATE TABLE IF NOT EXISTS beneficiaries (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT,
    age          INTEGER,
    education    TEXT,
    support_type TEXT
);

-- Registered volunteers
CREATE TABLE IF NOT EXISTS volunteers (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT,
    role    TEXT,
    contact TEXT
);

-- Donation transactions
CREATE TABLE IF NOT EXISTS donations (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    donor   TEXT,
    amount  INTEGER,
    purpose TEXT
);
```

---

## 🔁 Application Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Login page |
| `GET` | `/dashboard` | Metrics overview |
| `GET / POST` | `/beneficiaries` | List all / add new beneficiary |
| `GET` | `/delete-beneficiary/<id>` | Delete beneficiary by ID |
| `GET / POST` | `/volunteers` | List all / add new volunteer |
| `GET` | `/delete-volunteer/<id>` | Delete volunteer by ID |
| `GET / POST` | `/donations` | List all / add new donation |
| `GET` | `/delete-donation/<id>` | Delete donation by ID |

---

## 📸 Screenshots

### 🔐 Login Page
![Login](https://github.com/user-attachments/assets/9eca95e8-9f85-484f-93ec-fd9006ea66ef)

### 📊 Dashboard Overview
![Dashboard](https://github.com/user-attachments/assets/7512efa6-3403-44d3-8d83-8efa58923af7)

### 👨‍🎓 Beneficiary Management
![Beneficiaries](https://github.com/user-attachments/assets/e4d75a8b-e8e6-450e-b5f7-ae2c339e0aeb)

### 🤝 Volunteer Management
![Volunteers](https://github.com/user-attachments/assets/8252f4c6-712a-4f35-99bb-213283a5cdfd)

### 💰 Donation Management
![Donations](https://github.com/user-attachments/assets/036a56e0-0416-4b1c-bccc-2ad061f4db86)

---

## 🧠 Software Engineering Principles Applied

This project is a practical demonstration of core SEPM concepts:

- **Separation of Concerns** — Presentation (templates), logic (Flask routes), and data (SQLite + `database.py`) are cleanly decoupled
- **MVC-Inspired Architecture** — Models via SQLite schema, Views via Jinja2 templates, Controllers via Flask route handlers
- **DRY Templating** — `base.html` serves as a single master layout; all pages extend it via `{% block content %}`
- **CRUD Data Modeling** — Full Create, Read, and Delete operations across all three entities
- **Iterative Design** — Prototype-first approach with a clearly defined roadmap for production hardening
- **Extensible Schema** — Database tables designed with `AUTOINCREMENT` PKs and `IF NOT EXISTS` guards for safe re-initialization

---

## 🔮 Roadmap

The following enhancements are planned for future iterations:

- [ ] **Secure Authentication** — Server-side session management with `flask-login`, bcrypt password hashing, and DB-backed user accounts
- [ ] **Role-Based Access Control** — Separate Admin and Volunteer roles with scoped permissions
- [ ] **Edit / Update Records** — Full CRUD (currently Create, Read, Delete only)
- [ ] **Search & Filter** — Query beneficiaries by support category, volunteers by role, donations by date range
- [ ] **PDF & Excel Exports** — Automated report generation for field use and audit trails
- [ ] **Data Visualization** — Integrated charts (Chart.js / Matplotlib) on the dashboard for trend analysis
- [ ] **Mobile-Responsive UI** — Media queries and flex/grid layout for tablet and mobile access
- [ ] **Multi-Language Support** — Internationalization for regional NGO deployments
- [ ] **Deployment Guide** — Dockerized setup + hosting instructions (Render / Railway / VPS)

---

## 🎓 Academic Context

NGOConnect was developed as a capstone project for the **Software Engineering and Project Management (SEPM)** course. It applies the following concepts in a real-world context:

- Requirements elicitation and system scope definition
- Entity-Relationship modeling and database normalization
- Full-stack web application development
- UI/UX design for non-technical end users
- Prototype development with a defined path to production readiness
- Societal impact through digital transformation of civil society operations

---

## 📄 License

```
MIT License

Copyright (c) 2026 NGOConnect

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

> This project is intended strictly for **academic and educational purposes**.

---

<div align="center">

Built with 💚 for NGOs · Powered by Flask + SQLite · © 2026 NGOConnect

</div>
