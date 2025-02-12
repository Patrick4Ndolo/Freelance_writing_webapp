📖 Freelance Writing Web Application

A full-stack web application designed for managing freelance writing assignments, connecting clients, writers, editors, and admins seamlessly. The system allows clients to post assignments, admins to manage workflows, writers to take orders, and editors to review submitted work.
🚀 Project Overview

This platform streamlines the freelance writing process by offering:

    Client Dashboard: Post assignments, track progress, and receive completed work.
    Admin Dashboard: Manage assignments, track payments, and assign work to writers.
    Writer Dashboard: Browse available orders, submit completed work, and manage revisions.
    Editor Dashboard: Review, approve, or request revisions for assignments.
    Integrated Payment System: Clients make upfront payments, and writers receive one-third of the assignment price.

🎯 Key Features

✅ User Roles:

    Clients: Create assignments, track status, download completed work.
    Admins: Assign work to writers, manage users, track payments, and handle disputes.
    Writers: View available assignments, submit work, and respond to revisions.
    Editors: Review submitted assignments and approve or request changes.

✅ Assignment Lifecycle:

    Clients post assignments.
    Admins assign orders to writers with a single click.
    Writers complete and submit assignments.
    Editors review and finalize the work.
    Clients receive completed assignments.

✅ Payment System:

    Clients pay upfront (30%).
    Writers are paid one-third of the assignment fee.
    Payments are processed via a secure payment gateway.

✅ Real-Time Notifications:

    Users get alerts when assignments are updated, submitted, or approved.

✅ File Management:

    Upload & download client briefs, writer submissions, and editor feedback.

✅ Admin Control & Analytics:

    Monitor assignments, user performance, and financial transactions.

🛠 Technology Stack
Backend:

    Flask (Python) - Web framework
    Flask-SQLAlchemy - ORM for database interactions
    Flask-Login - User authentication
    SQLAlchemy - Database management
    Jinja2 - Template rendering engine

Frontend:

    HTML5, CSS3, Bootstrap - UI design
    JavaScript - Client-side interactivity

Database:

    SQLite / PostgreSQL (configurable)

Additional Libraries:

    Flask-WTF - Form handling
    Werkzeug - Secure password hashing
    Flask-SocketIO - Real-time notifications
    Stripe/PayPal API - Payment processing (if integrated)
