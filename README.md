# Hospital Management System

This is my first project in Web Development, built after learning the basics of Web and DBMS. The system includes three separate dashboards for the Admin, Doctors, and Patients. The main feature is the appointment booking system, where doctors set their availability for the next 7 days and patients can book morning or evening slots accordingly. The application also supports secure login and the storage of patient medical records.

## Technologies Used
* Flask
* SQLAlchemy
* Jinja2
* Bootstrap 5
* SQLite
* Python DateTime module

## Key Learnings
* I learned how to create a database schema with relational tables like User, Department, and Appointments.
* I understood how to use One-to-Many relationships to link doctors to departments and patients to their records.
* I gained experience using the Python DateTime module to manage scheduling logic for morning and evening time slots.
* I learned how to build role-based access to ensure users only see the dashboard related to their specific role.
* I learned how to handle the flow of data from a patient booking an appointment to a doctor providing a diagnosis and prescription.
