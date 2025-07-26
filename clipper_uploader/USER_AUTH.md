# C++ Video Clipper User Authentication and Registering (Module 2: Cloud Database)

## Overview

This module builds upon the foundational video clipper tool developed in Module 1. It introduces user authentication and registration using a cloud-hosted MongoDB Atlas database and Python. The goal of this module is to demonstrate how C++ applications can be integrated with external services (like a NoSQL cloud database) through system-level calls and Python scripts.

The enhanced application requires users to log in or register before they can access the core video clipping functionality. Authentication is performed through a terminal-based Python interface that securely handles user credentials.

## Unique Module Requirements Met

This software demonstrates the following requirements for the Cloud Database module:

- **Connection to a Cloud NoSQL Database:** Uses MongoDB Atlas to store user credentials.
- **Authentication:** Implements a login/registration system that interacts with the cloud database.
- **Python Integration:** Uses a Python script (`user_auth.py`) to handle database logic, triggered from C++.
- **Secure Credential Handling:** Passwords are hashed using SHA-256 before being stored.
- **Software Integration:** The C++ application only proceeds if the user successfully logs in or registers.
- **Create a cloud database with at least one table:** A MongoDB Atlas cluster is set up online, with a dedicated collection (analogous to a table in SQL) for storing user credentials.
- **Insert data into the cloud database:** When a new user registers, their username and hashed password are securely inserted into the MongoDB collection via the Python authentication script.
- **Modify data in the cloud database:** Users can update their password by re-registering or using a password reset feature, which updates the corresponding document in the database.
- **Delete data in the cloud database:** User accounts can be deleted from the database, removing their credentials from the collection.
- **Retrieve/query data from the cloud database:** During login, the Python script queries the database to verify the entered username and hashed password against stored records.
- **Software is written and executable:** The C++ and Python code is fully implemented, tested, and can be executed as described in the instructions.
- **Cloud DB used meaningfully in workflow:** The cloud database is essential for authentication; users must log in or register before accessing the main application features.
- **Uses appropriate tools/libraries:** The solution uses MongoDB Atlas, `pymongo` for database operations, and `python-dotenv` for secure environment variable management.
- **Implement user authentication:** The application enforces authentication by requiring users to log in or register, with credentials securely handled and verified against the cloud database.

[Clipper Register and Log in function](https://youtu.be/GaZZ1mwws9g)

## Development Environment

- **Visual Studio Code** was used for C++ development.
- **Python 3** was used to implement the login system (`user_auth.py`).
- MongoDB Atlas cluster was set up online and accessed using `pymongo` and `dotenv` packages.

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

- **MongoDB Atlas account and cluster** with connection string.
- **Python 3** installed locally.
- Python packages installed:
  ```bash
  pip install pymongo python-dotenv
  ```
- A `.env` file in the root of your project with your connection URI:
  ```env
  MONGO_URI=mongodb+srv://<username>:<password>@yourcluster.mongodb.net/?retryWrites=true&w=majority
  ```

## How to Run

1. Clone or download the project folder.
2. Ensure the `.env` file is properly configured.
3. Compile your C++ project as normal (see Module 1 README).
4. Run the C++ executable. It will automatically launch the Python login system.
5. Use the terminal interface to register or log in.
6. If successful, the program continues to the video clipping interface.

## Useful Websites

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - NoSQL cloud database platform.
- [pymongo Docs](https://pymongo.readthedocs.io/en/stable/) - Python MongoDB client documentation.
- [dotenv PyPI](https://pypi.org/project/python-dotenv/) - For managing environment variables securely.
- [SHA-256 Explanation](https://en.wikipedia.org/wiki/SHA-2) - Overview of password hashing method.