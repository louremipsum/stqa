# 1. Introduction

## 1.1 Purpose
This Software Requirements Specification (SRS) document provides a detailed description of the Todo List Application, including its functionality, features, and system requirements. The purpose of this application is to help users manage their tasks efficiently through a user-friendly web interface.

## 1.2 Scope
The Todo List Application will provide features for users to create, manage, and organize their tasks. It will support user authentication through login and signup functionality, with different roles assigned to users (admin, super admin, and regular user). The application will have a responsive design suitable for both desktop and mobile devices.

## 1.3 Audience
This document is intended for project stakeholders, including developers, project managers, and potential users of the application.

# 2. Overall Description

## 2.1 Product Perspective
The Todo List Application is a standalone web application that interacts with a MySQL database for persistent storage. The application will utilize Node.js and Express for backend processing and Passport.js for user authentication.

## 2.2 Product Functions

### User Authentication:
- Signup functionality for new users
- Login functionality for existing users
- Role-based access control (admin, user)

### Task Management:
- Create, update, and delete tasks
- Mark tasks as complete or incomplete
- View and filter tasks by status (all, active, completed)
- Clear completed tasks

### User Interface:
- User-friendly task management interface

## 2.3 User Classes and Characteristics
- **Admin:** See all users who are users and their percentage of task completion.
- **User:** Can create and manage their own tasks.

## 2.4 Operating Environment
- Web browsers (Chrome, Firefox, Safari, Edge)
- Mobile devices (responsive design)
- Server with Node.js and MongoDB support

## 2.5 Design and Implementation Constraints
- The application must comply with web accessibility standards.
- Must be developed using the specified technologies (HTML, CSS, JavaScript, Node.js, Express, MongoDB).

# 3. Specific Requirements

## 3.1 Functional Requirements

### 3.1.1 User Authentication
- **FR-1:** The system shall allow users to sign up with a unique username and password.
- **FR-2:** The system shall authenticate users through a login form.
- **FR-3:** The system shall assign roles (admin, user) upon signup.
- **FR-4:** The system shall redirect users to the appropriate dashboard based on their role after login.

### 3.1.2 Task Management
- **FR-5:** Users shall be able to create a new task with a title and description.
- **FR-6:** Users shall be able to edit existing tasks.
- **FR-7:** Users shall be able to delete tasks.
- **FR-8:** Users shall be able to mark tasks as complete or incomplete.
- **FR-9:** Users shall be able to view all tasks, completed tasks, or active tasks.
- **FR-10:** Users shall be able to filter tasks by status using provided buttons.
- **FR-11:** Users shall be able to clear all completed tasks in one action.

# 4. External Interface Requirements

## 4.1 User Interfaces
Web-based interface that includes:
- Signup/Login forms
- Task management dashboard
- Navigation for filtering tasks

## 4.2 Hardware Interfaces
The application will run on standard web server hardware that supports Node.js and MongoDB.

## 4.3 Software Interfaces
- MongoDB database for task storage.
- Node.js and Express framework for backend development.

# 5. Use Cases

## 5.1 Use Case Descriptions

### Use Case: User Signup
- **Actor:** New User
- **Description:** The user enters their details to create an account.
- **Precondition:** User must not have an existing account.
- **Postcondition:** A new user account is created.

### Use Case: Task Creation
- **Actor:** Logged-in User
- **Description:** The user creates a new task.
- **Precondition:** User must be logged in.
- **Postcondition:** A new task is added to the user's task list.

# 6. Appendix

## 6.1 References
- HTML
- CSS
- JavaScript
- Node.js
- Express
- MongoDB

## 6.2 Glossary
- **CRUD:** Create, Read, Update, Delete
- **UI:** User Interface

## Screen Shots
![image](https://github.com/user-attachments/assets/88e0d989-342b-402e-99c1-ca73b31355ec)
![image](https://github.com/user-attachments/assets/dfe5dcad-9c7d-458b-8835-e7ad403d99ce)
![image](https://github.com/user-attachments/assets/483baa08-e46f-4598-8752-ecf46546fcb3)
![image](https://github.com/user-attachments/assets/1b9c9b0b-7b6d-4348-85d7-e99a98cf109f)
![image](https://github.com/user-attachments/assets/1646ebcd-f125-4fa4-aa14-59b774637902)
![image](https://github.com/user-attachments/assets/151c2bc8-db29-45c9-b6c4-78be154c44e2)
![image](https://github.com/user-attachments/assets/39daac8f-10e5-46ac-bf5e-4e78e9eba859)

## Active Tasks

![image](https://github.com/user-attachments/assets/f31a8bcb-1d68-4f8e-a600-43a910776394)

## Completed Task

![image](https://github.com/user-attachments/assets/75abe00f-4052-428c-bf49-103820a0fc94)

## Clear Completed

![image](https://github.com/user-attachments/assets/2d6f79e7-90a2-4e0b-a201-7373ead41ffe)

## Admin

![image](https://github.com/user-attachments/assets/c98bdcf4-92ec-486e-9070-9e8c71adb179)


## Testing ScreenShot
![Screenshot 2024-10-08 180607](https://github.com/user-attachments/assets/9ba475a1-6bad-4461-9f63-155bf5816bdf)
![Screenshot 2024-10-08 173742](https://github.com/user-attachments/assets/8021b6f6-9cb2-440a-bafb-d879a26e5839)
![Screenshot 2024-10-08 174516](https://github.com/user-attachments/assets/24efb4d1-a71d-4e1e-9067-da53a4619379)
![Screenshot 2024-10-08 174755](https://github.com/user-attachments/assets/5c0d527d-1037-491b-83f3-f9fd33c1e6e4)
