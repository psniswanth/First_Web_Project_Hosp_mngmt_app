# Hospital Management System (HMS)

Hi! This is my first full-stack project, built after learning the fundamentals of Web Development and DBMS. [cite_start]I created this system to simplify the communication between hospital administrators, doctors, and patients[cite: 9].

## 🏥 About the Project
[cite_start]The application is a comprehensive management tool that supports secure user authentication and role-based access[cite: 10]. It features three distinct dashboards:
* [cite_start]**Admin Dashboard:** For high-level system oversight[cite: 9].
* [cite_start]**Doctor Dashboard:** For managing schedules and patient records[cite: 13, 18].
* [cite_start]**Patient Dashboard:** For booking appointments and viewing medical history[cite: 13, 18].

The "highlight" feature is the **Smart Appointment System**. [cite_start]Doctors can set their availability for upcoming dates, and patients can seamlessly book morning or evening slots based on that real-time data[cite: 13, 20].

## 🛠️ Tech Stack
* [cite_start]**Backend:** Python-Flask [cite: 13]
* [cite_start]**Database:** SQLite with SQLAlchemy ORM [cite: 13]
* [cite_start]**Frontend:** Bootstrap 5, Jinja2, HTML, and CSS [cite: 6, 13]
* [cite_start]**Scheduling:** Python DateTime module [cite: 13]

## 🧠 Key Learnings
Building this project from scratch taught me several core concepts:
* [cite_start]**Relational Database Design:** I learned how to structure data using One-to-Many relationships, such as linking departments to doctors and patients to their specific appointment history[cite: 21, 22, 23].
* [cite_start]**CRUD Implementation:** I gained experience performing Create, Read, Update, and Delete operations—from registering new users to logging complex medical records like diagnoses and prescriptions[cite: 18, 27].
* [cite_start]**Role-Based Logic:** I implemented logic to ensure that different users see only the data relevant to them, managed through backend session handling[cite: 10, 16].
* [cite_start]**Scheduling Logic:** I used the DateTime module to handle time-slot logic, ensuring that morning and evening availability is tracked accurately for every doctor[cite: 13, 52, 54].

## 📂 Database Schema
[cite_start]The system is built on a relational backend with the following key tables[cite: 11, 15]:
* [cite_start]**User:** Handles authentication, roles (Admin/Doctor/Patient), and status[cite: 16, 17].
* [cite_start]**Department:** Organizes hospital specializations[cite: 18].
* [cite_start]**Appointments:** Stores all visit details, including symptoms, tests done, and medicine prescribed[cite: 18, 27].
* [cite_start]**DoctorAvailability:** Tracks specific date-based slots for the medical staff[cite: 19, 20].

## 🚀 Getting Started
1. **Clone the repository:**
   git clone https://github.com/your-username/hms-project.git
2. **Install dependencies:**
   pip install flask flask-sqlalchemy
3. **Run the app:**
   python app.py
