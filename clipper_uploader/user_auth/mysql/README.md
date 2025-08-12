# C++ Video Clipper User Authentication and Registering (Module 3: SQL Relational Database)

## Overview

This module builds upon the foundational video clipper tool developed in Module 1. It introduces user authentication and registration using a MySQL relational database and Python. The goal of this module is to demonstrate how C++ applications can be integrated with a relational database backend through system-level calls and Python scripts.

The enhanced application requires users to log in or register before they can access the core video clipping functionality. Authentication is performed through a terminal-based Python interface that securely handles user credentials and stores them in MySQL.

---

## Unique Module Requirements Met

This software demonstrates the following requirements for the SQL Relational Database module:

- **Connection to a SQL Database:** Uses MySQL to store user credentials and account creation dates.
- **Authentication:** Implements a login/registration system that interacts with the MySQL database.
- **Python Integration:** Uses a Python script (`user_auth.py`) to handle database logic, triggered from C++.
- **Secure Credential Handling:** Passwords are hashed using SHA-256 before being stored, and database credentials are kept in a `.env` file (ignored by GitHub).
- **Software Integration:** The C++ application only proceeds if the user successfully logs in or registers.
- **Create a relational database with at least one table:** A MySQL database (`user`) is created locally, with a table `accounts` containing username, hashed password, and `created_at` fields.
- **Insert data into the database:** When a new user registers, their username, hashed password, and account creation date are stored in the database via the Python authentication script.
- **Modify data in the database:** Users can update their username or password securely through menu options.
- **Delete data in the database:** User accounts can be deleted from the database, removing their credentials.
- **Retrieve/query data from the database:** During login, the Python script queries the database to verify the entered username and hashed password. The account creation date is also displayed.
- **Query data by date/time:** A menu option allows filtering accounts created within a specific date range.
- **Software is written and executable:** The C++ and Python code is fully implemented, tested, and can be executed as described in the instructions.
- **SQL DB used meaningfully in workflow:** The database is essential for authentication; users must log in or register before accessing the main application features.
- **Uses appropriate tools/libraries:** The solution uses MySQL, `mysql-connector-python` for database operations, and `python-dotenv` for secure environment variable management.
- **Implement user authentication:** The application enforces authentication by requiring users to log in or register, with credentials securely handled and verified against the MySQL database.

[Clipper Register and Log in function](#) <!-- Replace with your actual video link -->

---

## Development Environment

- **Visual Studio Code** was used for C++ development.
- **Python 3** was used to implement the login system (`user_auth.py`).
- **MySQL Server** was installed locally and accessed using `mysql-connector-python` and `dotenv`.

The `main()` function in the C++ application includes the following authentication call:

```cpp
std::cout << "🔐 Launching login system...\n";
int auth_result = system("python user_auth.py");
if (auth_result != 0) {
    std::cout << "👋 Exiting app.\n";
    return 0;
}
std::cout << "✅ Authenticated!\n";
```

## Prerequisites

Before running this module, ensure you have the following configured:

- **MySQL WorkBench 8.0 CE** installed locally and running.
- **Python 3** installed locally.
- Python packages installed:
  ```bash
  pip install mysql-connector-python python-dotenv
  ```
- A `.env` file in the root of your project  your database credentials (this file should be in `.gitignore` so it’s not uploaded to GitHub):
  ```env
  MYSQL_HOST=localhost
  MYSQL_PORT=3306
  MYSQL_USER=root
  MYSQL_PASSWORD=your_mysql_password
  MYSQL_DB=user
  ```

- MySQL database and table created:
```sql
CREATE DATABASE user_db;
USE user_db;

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

## Useful Websites

- [MySQL](https://dev.mysql.com/) - SQL database platform.
- [mysql-connector-python Docs](https://dev.mysql.com/doc/connector-python/en/) - Python MySQL client documentation.
- [dotenv PyPI](https://pypi.org/project/python-dotenv/) - For managing environment variables securely.
- [SHA-256 Explanation](https://en.wikipedia.org/wiki/SHA-2) - Overview of password hashing method.