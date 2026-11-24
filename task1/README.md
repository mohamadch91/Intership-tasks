# Task 1: Library Management System API (Django)

## Overview
In this task, you will design and develop a **Library Management System** backend using **Django** and **Django REST Framework (DRF)**. The system includes custom user management, role-based access control (RBAC), book inventory management, a request-and-approval borrowing workflow, and an author book submission feature.

---

## 1. User Management & Authentication

### User Model
The default Django user model must be replaced with a custom User model (extending `AbstractBaseUser` / `AbstractUser`):
- **Phone Number (`phone`)**: Unique identifier that serves as the **username** for authentication (instead of standard username or email).
- **First Name (`first_name`)**: String, required.
- **Last Name (`last_name`)**: String, required.
- **Photo (`photo`)**: Image field for profile photo (optional/nullable).
- **Role (`role`)**:
  - `client`: Regular library user / patron.
  - `administration`: Administrator with management permissions.
  - `author`: Author user type (see [Section 4](#4-author-user-feature)).

### User APIs
- **Register (`POST /api/users/register/`)**:
  - Register with phone number, password, first name, last name, and optional photo.
- **Login (`POST /api/users/login/` or `/api/token/`)**:
  - Authenticate using phone number and password (JWT or Token authentication).
- **Update User (`PUT/PATCH /api/users/profile/`)**:
  - Update user details and/or upload a new profile photo.
- **Delete User Photo (`DELETE /api/users/profile/photo/`)**:
  - Remove the user's existing photo without deleting the user account.

---

## 2. Book Management

### Book Model
Each book must include:
- **Name / Title (`name` / `title`)**: String, required.
- **Author (`author`)**: Author name (or ForeignKey to author user/model).
- **ISBN (`isbn`)**: Unique ISBN code.
- **Additional Necessary Fields**:
  - Description / Summary (`description`)
  - Published Date (`published_date`)
  - Genre / Category (`genre` / `category`)
  - Quantity / Available Copies (`total_copies`, `available_copies`)
  - Status / Approval Status (`status` / `is_approved`: e.g., pending, approved, rejected)

### Book APIs & Permissions
- **List / View Books (`GET /api/books/`, `GET /api/books/<id>/`)**:
  - Accessible to users to view approved books in the catalog.
- **Add Book (`POST /api/books/`)**:
  - **Permission**: Only `administration` users can directly add and publish books (see [Section 4](#4-author-user-feature) for author contributions).
- **Update Book (`PUT/PATCH /api/books/<id>/`)**:
  - **Permission**: Only `administration` users can update book details.
- **Delete Book (`DELETE /api/books/<id>/`)**:
  - **Permission**: Only `administration` users can delete books.
- **Borrow Book (`POST /api/books/<id>/borrow/` or Borrow Request API)**:
  - Accessible to `client` users (subject to approval workflow below).

---

## 3. Borrowing Workflow

Regular users cannot directly borrow a book without administrative approval. The borrowing process follows a request-and-approval flow:

1. **Borrow Request (Client)**:
   - A `client` user submits a borrow request for a book.
   - The request is created with status `PENDING`.
2. **Administration Approval**:
   - Only `administration` users can review pending borrow requests.
   - The administrator can **Accept** or **Reject** the request.
3. **Borrow Completion**:
   - Once accepted by administration, the book is marked as `BORROWED` (and available inventory is decremented).
   - Borrow date and due date are recorded.
4. **Return Book (Standard Flow)**:
   - Returning the book marks the borrow record as returned and restores inventory.

---

## 4. Author User Feature

An additional user role: **Author**.
- **Role**: `author`
- **Book Submission**:
  - Author-type users can add new books to the system.
- **Administration Confirmation Required**:
  - When an author adds a book, the book is submitted for review with status `PENDING_APPROVAL` (or `is_approved=False`).
  - The book is **not** visible or available for borrowing in the public catalog until an `administration` user reviews and accepts/confirms it.
  - Once confirmed by administration, the book becomes published and available in the library catalog.

---

## Role Permissions Summary

| Action | Client | Author | Administration |
| :--- | :---: | :---: | :---: |
| Register / Login | Yes | Yes | Yes |
| Update Profile / Delete Photo | Self only | Self only | Any / Self |
| View Approved Books | Yes | Yes | Yes |
| Request Book Borrow | Yes | Yes | Yes |
| Approve / Reject Borrow Requests | No | No | Yes |
| Add Book | No | Yes (requires admin approval) | Yes (direct) |
| Update / Delete Book | No | No | Yes |
| Confirm / Approve Author Books | No | No | Yes |

---

## Git Workflow & Submission

1. **Do not commit directly to `main`**. The `main` branch is protected.
2. Create and switch to a separate task branch:
   ```bash
   git checkout -b task-1
   ```
3. Implement the Django project, models, views/viewsets, serializers, permissions, and tests.
4. Push your branch and open a Pull Request (PR) against `main` for review.
