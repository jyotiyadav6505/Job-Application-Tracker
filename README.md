# 💼 Job Application Tracker

A Streamlit-based web application to track, manage, and analyze job and internship applications in one place.

The application uses SQLite for data storage and provides a simple dashboard to monitor application progress.

---

## 🚀 Features

### 📊 Dashboard
- Total applications
- Interview count
- Offer count
- Rejected applications
- Interview rate
- Offer rate
- Application status chart

### ➕ Add Applications
Track important details such as:
- Company name
- Job role
- Location
- Application date
- Job link
- Application status
- Interview date
- Notes

### 📋 Application Management
- View all saved applications
- Search by company or job role
- Filter applications by status
- Edit existing applications
- Delete applications

### 📥 CSV Export
Download all application records as a CSV file for further analysis in Excel or other spreadsheet applications.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **SQLite**
- **Pandas**

---

## 📁 Project Structure

```text
Job Application Tracker/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── applications.db
│
└── screenshots/
    ├── dashboard.png
    ├── add_application.png
    └── applications.png


    