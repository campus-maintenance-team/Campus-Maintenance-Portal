# Campus Maintenance Portal

A web-based complaint management system designed for campuses, hostels, or residential societies. The application allows users to submit maintenance issues and enables administrators to track, manage, and resolve them efficiently.

---

## Overview

The Campus Maintenance Portal provides a centralized platform where residents can report problems such as plumbing, electrical, or other maintenance issues. Each complaint is assigned a unique ticket ID so that it can be tracked and managed easily by the admin team.

This project demonstrates the integration of frontend technologies with a Python backend using Flask.

---

## Live Demo

Live Project:
https://campus-maintenance-portal.onrender.com

---

## Features

- Submit maintenance complaints through a structured form
- Automatic generation of unique ticket IDs
- Categorized complaints (Plumbing, Electrical, etc.)
- Priority level selection
- Detailed complaint description
- Admin dashboard to view submitted tickets
- Organized data structure for easy issue management
- Responsive and user-friendly interface

---

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Flask

Other Tools:
- Fetch API for frontend-backend communication
- JSON data handling

---

## Project Structure

```
campus-maintenance-portal
│
├── static
│   ├── css
│   │   ├── admin.css
│   │   └── style.css
│   └── js
│       ├── admin.js
│       └── script.js
│
├── templates
│   ├── index.html
│   └── admin.html
│
├── app.py
├── maintenance_db.json
├── requirements.txt
└── README.md
```

---

## Screenshots

### Complaint page
![](screenshots/User-1.png)
![](screenshots/User-2.png)

### Admin page
![](screenshots/Admin-1.png)
![](screenshots/Admin-2.png)

---

## How It Works

1. A user fills out the complaint form.
2. The form data is sent to the Flask backend.
3. The backend generates a unique ticket ID.
4. The complaint details are stored.
5. Admin can view all submitted complaints through the admin panel.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/campus-maintenance-portal.git
```

### 2. Navigate to the project folder

```bash
cd campus-maintenance-portal
```

### 3. Install required dependencies

```bash
pip install flask
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

## Example Complaint Fields

- Name
- Email
- Phone Number
- Block
- Floor
- Room Number
- Issue Category
- Additional Details
- Priority Level
- Issue Date

## Future Improvements

- User authentication system
- Admin login panel
- Ticket status tracking (Open, In Progress, Resolved)
- Email notifications
- Database integration (MySQL / PostgreSQL)
- AI-based complaint categorization
- Deployment on cloud platforms

## Learning Objectives

This project was built to practice:

- Full stack web development
- Flask backend integration
- JavaScript Fetch API
- Form handling and validation
- Building structured web applications

## Author

