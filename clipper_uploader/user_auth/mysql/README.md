# Overview

This project enhances a C++ desktop video clipping application by integrating a secure user authentication system connected to a MySQL relational database. The purpose of this software is to build skills in database-driven application development, cross-language integration, and secure credential handling.

The program launches with a Python-based login system that interacts with a MySQL backend, requiring users to register or log in before accessing the video clipping tools. All credentials are hashed using SHA-256 for security, and database connection settings are stored in a `.env` file to prevent exposure in public repositories.

The software demonstrates the ability to:
- Connect to a relational database.
- Perform CRUD operations (create, read, update, delete).
- Filter data based on a date range.
- Integrate Python scripts into a C++ workflow.

Once authenticated, users can process video clips through a menu-driven interface that uses FFmpeg for media handling.

[Register and Log in function](https://youtu.be/DyD1pGXMxMU)

# Relational Database

The application uses a **MySQL** database running locally.
Database: `users`
Table: `accounts`

The `accounts` table contains the following columns:
- **id** (INT, Primary Key, Auto Increment) – Unique identifier for each account.
- **username** (VARCHAR) – Unique username chosen by the user.
- **password** (VARCHAR) – SHA-256 hashed password.
- **created_at** (DATETIME) – Automatically set when the account is created.

This structure allows secure storage of user data and supports queries to filter accounts by creation date.

# Development Environment

- **C++** – Core application for video clipping, built in Visual Studio Code.
- **Python 3** – Authentication and MySQL interaction (`user_auth.py`).
- **MySQL Server** – Local instance for relational data storage.
- **Libraries Used**:
  - `mysql-connector-python` – For Python to MySQL communication.
  - `python-dotenv` – For secure environment variable management.
  - `hashlib` – For password hashing.
- **External Tools**:
  - `.env` file – Stores MySQL credentials securely (ignored by GitHub).

# Useful Websites

- [MySQL Official Site](https://dev.mysql.com/)
- [mysql-connector-python Documentation](https://dev.mysql.com/doc/connector-python/en/)
- [Python Dotenv PyPI](https://pypi.org/project/python-dotenv/)
- [SHA-256 Hashing Explanation](https://en.wikipedia.org/wiki/SHA-2)

# Future Work

- Add password reset functionality with email verification.
- Implement pagination and search for account listing.
- Integrate cloud-hosted MySQL to allow remote authentication.
- Improve the C++ interface for a more user-friendly GUI.
- Add more video processing features beyond clipping.

## Prerequisites

Before running this module, ensure you have the following configured:

- **MySQL WorkBench 8.0 CE** installed locally and running.
- **Python 3** installed locally.
- Python packages installed:
  ```bash
  pip install mysql-connector-python python-dotenv
  ```
- A `.env` file in the root of your project your database credentials (this file should be in `.gitignore` so it’s not uploaded to GitHub):

  ```env
  MYSQL_HOST=localhost
  MYSQL_PORT=hostnumber
  MYSQL_USER=root
  MYSQL_PASSWORD=your_mysql_password
  MYSQL=users
  ```

- MySQL database and table created:

```sql
CREATE DATABASE users;
USE users;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## How to Run

1. Clone or download the project folder.
2. Ensure the `.env` file is properly configured with your MySQL credentials.
3. Compile your C++ project as normal (see Module 1 README).
4. Run the C++ executable. It will automatically launch the Python login system.
5. Use the terminal interface to:

- **Register a new account**
- **Log in to an existing account**
- **Update usarname/password**
- **Delete account**
- **Show accounts created within a date range**

6. If successful, the program continues to the video clipping interface.
