# User Management Documentation

## Table of Contents
1. [Models](#models)
   - [User Model](#user-model)
2. [Views](#views)
   - [Index](#index)
   - [Microsoft Login](#microsoft-login)
   - [Logout](#logout)
   - [Login](#login)
   - [Profile](#profile)
   - [Deactivated User](#deactivated-user)
   - [Administrator Dashboard](#administrator-dashboard)
   - [Basic User Dashboard](#basic-user-dashboard)
   - [Change Username](#change-username)
   - [User Management](#user-management)
   - [Home](#home)

---

## Models
### User Model
This module defines the `User` model for the application using Django’s ORM (`django.db.models`). It maps Python class objects to relational database tables.

#### Attributes:
- `email`: `char(255)`, **Primary Key** – Unique identifier for the user.
- `name`: `char(255)` – User's full name.
- `role`: `char(45)` – Role assigned to the user (`Administrator` or `Basicuser`).
- `status`: `char(1)` – Account status:
  - `'0'` – Deactivated
  - `'1'` – Active

---

## Views

### Index
**Function:** `index()`
- **Input:** HTTP request
- **Output:** Renders `index.html`
- **Description:** Displays the Microsoft login button, which redirects the user to [`microsoft_login()`](#microsoft-login).

### Microsoft Login
**Function:** `microsoft_login()`
- **Input:** HTTP request
- **Output:** Redirects to Microsoft login page through Microsoft Azure.

### Logout
**Function:** `logout_view()`
- **Input:** HTTP request
- **Output:** Redirects to Microsoft logout page through Microsoft Azure.

### Login
**Function:** `login_view()`
- **Input:** HTTP request
- **Description:** Handles Microsoft OAuth authentication callback.
- **Process:**
  1. Retrieves authentication code from the request.
  2. Exchanges the code for an access token.
  3. Fetches user details from the Microsoft Graph API.
  4. Checks database:
     - If user does not exist, create a new entry and assign `Administrator` role if they are the first user.
     - If user exists, retrieve their details from the database.
  5. User Status Check:
     - If `status = '0'`, redirect to [`Deactivated_user()`](#deactivated-user).
     - If `status = '1'`, redirect to [`home()`](#home).

### Profile
**Function:** `profile()`
- **Input:** HTTP request
- **Description:** Confirms user role and redirects:
  - **Administrator:** Redirect to [`Administrator()`](#administrator-dashboard).
  - **Basicuser:** Redirect to [`Basicuser()`](#basic-user-dashboard).

### Deactivated User
**Function:** `Deactivated_user()`
- **Input:** HTTP request
- **Output:** Renders a page notifying the user that their account is deactivated.

### Administrator Dashboard
**Function:** `Administrator()`
- **Input:** HTTP request
- **Output:** Renders a page for `Administrator` with relevant controls.

### Basic User Dashboard
**Function:** `Basicuser()`
- **Input:** HTTP request
- **Output:** Renders a page for `Basicuser` with limited features.

### Change Username
**Function:** `changeUsername()`
- **Input:** HTTP request
- **Description:** Allows `Basicuser` to change their username.

### User Management
**Description:**
  The CRUD function is only applicable for `Administrator`.
  
**Functions:**
- `create_user()` – Adds a new user to the database.
- `update_user()` – Updates user details.
- `delete_user()` – Removes a user from the database.

### Home
**Function:** `home()` in the `Home` application
- **Input:** HTTP request
- **Output:** Renders the main home page for logged-in users.

---

**Note:** This documentation serves as a guide to understanding the User Management module, outlining its structure and functionality within the application.
