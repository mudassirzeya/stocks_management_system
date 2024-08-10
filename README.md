# Stock & Sales Management System
This project is a comprehensive Stock Management System built with Django. It allows organizations to manage their inventory and sales efficiently. The app provides features for managing customer data, processing sales, and generating invoices automatically.

# WebApp Images
![image](https://github.com/user-attachments/assets/8c21caad-dd6b-4e6c-813a-4815ec06f856)
![image](https://github.com/user-attachments/assets/b3fa9a76-1421-46a0-891e-694c89ff8146)
![image](https://github.com/user-attachments/assets/f64e729e-3993-4805-ad93-d2fca95860e3)
![image](https://github.com/user-attachments/assets/57f54c24-e31e-4072-b5bf-159d60e9d8aa)
![image](https://github.com/user-attachments/assets/7e16593f-a856-4aec-87c7-4f515a66b32a)








# Features
1) User Authentication: Users can log in with their credentials. New organizations can create an account and add team members.
2) Inventory Management: Employees can manage stock levels by adding, updating, and deleting products.
3) Customer Management: The system supports both new and returning customers, with customer data stored for future transactions.
4) Sales Processing: Employees can process sales transactions, select or add customers, and add products purchased by the customer.
5) Invoice Generation: The app automatically generates invoices with the customer's name and the total amount due, which can be printed directly.
6) Email Notification: Passwords for new employees are sent via email when added to the platform.

# Technologies Used
1) Backend: Django
2) Frontend: HTML, CSS, Bootstrap 4, JavaScript
3) Database: SQLite (default, can be changed)
4) Email Service: Django's Email backend (for sending passwords)

# Installation
1) Clone the Repository: git clone https://github.com/mudassirzeya/stocks_management_system.git
2) Create a Virtual Environment (It's recommended to use a virtual environment to manage dependencies).
   1) python3 -m venv venv
   2) source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3) Install Dependencies
   1) pip install django pillow
   2) pip install django-mathfilters
4) Configure the Database (By default, the app uses SQLite. You can configure another database in the settings.py file).
   1) python manage.py migrate
5) Set Up Email Backend
   1) Update the email configuration in the settings.py file to use your preferred email service for sending passwords.
6) Create Superuser (Admin Account)
   1) python manage.py createsuperuser
7) Run the Development Server
   1) python manage.py runserver

# Usage
### For Organizations:
  1) ** Sign up for a new account.
  2) Add employees to the platform.
  3) Employees will receive their login credentials via email.
### For Employees:
  1) Log in with the credentials sent via email.
  2) Manage stock by adding, updating, or deleting products.
  3) Process sales by selecting or adding customers and generating invoices.
### For Admins:
  1) Log in to the admin dashboard.
  2) View and manage inventory, sales records, customer data, and generated invoices.

# Example Workflow
1) Add New Products: Admins can add new products to the inventory, specifying details like name, quantity, and price.
2) Process a Sale: When a customer makes a purchase, select the customer (or add a new one), choose the products being bought, and generate an invoice.
3) Generate Invoice: The app will automatically calculate the total price and generate an invoice that can be printed or saved.

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to contribute to this project.
