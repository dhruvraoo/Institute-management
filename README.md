# Institute-management
A Python-based Institute Management System using PostgreSQL (psycopg2) and OOP principles, designed to manage students, faculty, and administration efficiently.

🔹 Features
Role-Based Access:
🛠 Admin: Registers Faculty and Students.
🎓 Principal: (Subclass of Faculty) Manages Faculty and Student data.
👨‍🏫 Faculty: Logs in but cannot register new users.
👨‍🎓 Students: Logs in but cannot register themselves.

Database-Driven:
Uses PostgreSQL with separate tables for Faculty, Students, and Marks.
OOP-Based Architecture:
Modular and scalable design using Object-Oriented Programming.

🚀 Technologies Used
Python
PostgreSQL (psycopg2)
Object-Oriented Programming (OOP)
