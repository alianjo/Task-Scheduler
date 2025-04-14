# Task Scheduler and Notification System

Welcome to the **Task Scheduler and Notification System** project! This is a learning project where you'll build a web application to schedule and manage tasks, using **Django REST Framework**, **Celery**, **RabbitMQ**, **Celery Beat**, and **Celery Worker**. Your goal is to create a system that lets users schedule tasks and track their progress while mastering these technologies. Let’s collaborate and make it awesome!

---

## 📋 Project Overview

The **Task Scheduler and Notification System** is a web app where users can:
- Create tasks (like sending emails or processing data).
- Schedule tasks to run at specific times or on a recurring basis.
- Track task statuses (e.g., pending, completed, failed).
- Receive notifications when tasks are done or encounter issues.

You’ll build this using **Django REST Framework** for the API, **RabbitMQ** as the message broker, **Celery** for running tasks in the background, **Celery Beat** for scheduling, and **Celery Worker** to process tasks.

---

## 🔑 Features and Technology Usage

The application should include these features, with specific technologies applied as follows:

1. **User Authentication**:
   - **Description**: Users can sign up and log in to manage their tasks securely.
   - **Technology**:
     - **Django REST Framework**: Build API endpoints for user registration and login (e.g., using token-based authentication like JWT or Django’s built-in sessions).
     - Use Django’s authentication system to handle user accounts and permissions.

2. **Task Creation**:
   - **Description**: Users can create tasks via a REST API, specifying a title, description, and when the task should run.
   - **Technology**:
     - **Django REST Framework**: Create API endpoints (e.g., `POST /api/tasks/`) to accept task details and save them to the database.
     - Store tasks in a database model with fields like title, description, and scheduled time.

3. **Task Scheduling**:
   - **Description**: Users can schedule tasks to run once (e.g., at 10 AM tomorrow) or periodically (e.g., every day).
   - **Technology**:
     - **Celery Beat**: Use Celery Beat to schedule tasks. Store scheduling details (e.g., one-time or periodic) in Celery Beat’s database and trigger tasks at the specified times.
     - **RabbitMQ**: Queue scheduling requests as messages to ensure tasks are processed reliably.
     - **Celery**: Define tasks that Celery Beat will trigger (e.g., a task to send an email at a specific time).

4. **Task Status Tracking**:
   - **Description**: Users can view their tasks and check statuses like "pending," "completed," or "failed" through the API.
   - **Technology**:
     - **Django REST Framework**: Build API endpoints (e.g., `GET /api/tasks/`) to list tasks and their statuses for the logged-in user.
     - **Celery**: Update task statuses in the database when tasks are processed (e.g., mark as "completed" after execution).
     - **RabbitMQ**: Ensure task status updates are queued and processed reliably.

5. **Email Notifications**:
   - **Description**: When a task finishes or fails, the system sends an email to the user with the result.
   - **Technology**:
     - **Celery**: Create a Celery task to send emails asynchronously (e.g., using Django’s `send_mail`).
     - **RabbitMQ**: Queue email tasks to handle sending notifications without delaying the main application.
     - **Celery Worker**: Run the Celery worker to process email tasks in the background, ensuring emails are sent efficiently.

---

## 🛠️ Technologies to Use

You must use these technologies to implement the features above:
- **Django REST Framework**: For building the REST API to handle user authentication, task creation, and task status tracking.
- **RabbitMQ**: As the message broker to queue tasks and updates for scheduling, status changes, and notifications.
- **Celery**: To process asynchronous tasks like sending emails and updating task statuses.
- **Celery Beat**: To schedule tasks for one-time or periodic execution.
- **Celery Worker**: To execute tasks in the background, ensuring smooth performance.


