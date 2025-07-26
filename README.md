# C++ Video Clipper (Module 1: Language - C++)  
_Also integrated in Module 2: Cloud Databases_

## Overview

As a software engineer, I am focused on mastering foundational programming through the C++ language. This project demonstrates my understanding of core C++ concepts, file system interactions, and external tool integration.

The console-based application acts as a video clipper. It takes a user-defined input video and extracts multiple clips based on start/end timestamps and a custom clip name. Each clip is saved into a uniquely named folder and sequentially numbered (e.g., `1_MyClipName.mp4`).

This tool uses FFmpeg under the hood for high-speed, lossless video clipping using stream copy (`-c:v copy -c:a copy`), and provides real-time console feedback during processing.

This project also forms the foundation for a larger system, where a user authentication layer (Module 2) enables access to the clipper. Future modules will integrate cloud databases (MongoDB Atlas) and YouTube video uploading.

## 🔒 User Authentication Integration (Module 2: Cloud Databases)

In Module 2, the clipper application was extended with a secure login/registration system using Python and a MongoDB Atlas cloud database. A Python script (`user_auth.py`) handles:

- Registering new users  
- Authenticating returning users  
- Validating passwords using SHA-256 hashing  
- Reading credentials securely using environment variables (`.env` file)

The C++ application calls this script first, using `system("python user_auth.py")`, and only continues if login is successful (Python returns code `0`). This integration demonstrates the use of cloud-hosted NoSQL databases in real software systems.

The MongoDB connection string is stored in a local `.env` file using `python-dotenv` to avoid hardcoding sensitive information.

✅ See `user_auth.py` for the Python authentication system.

✅ `.env` file format:
```ini
MONGO_URI=mongodb+srv://yourUser:yourPassword@yourCluster.mongodb.net/?retryWrites=true&w=majority
```

## Unique Module Requirements Met

This software demonstrates the following requirements for the C++ Language module:

- **Variables, Expressions, Conditionals, Loops, Functions, Classes:** Used extensively in the `VideoClipper` class and helper functions.
- **Data structure from STL:** `std::vector`, `std::string`, `std::array`, and `std::stringstream` are used for clip management, text processing, and output parsing.
- **Read and write to a file:** Uses `std::filesystem` to create output folders and verify paths.
- **Use the `new` and `delete` operators to dynamically create objects:** The `VideoClipper` object is created with `new` and cleaned up with `delete`.
- **Run external programs from C++:** FFmpeg is run using `_popen()` to provide real-time streaming of command-line output.
- **Interact with another programming language:** Integrates with Python via `system()` calls for login and user registration workflows.

[Clipper CPP Video](https://youtu.be/GaZZ1mwws9g)

## Development Environment

- **Language:** C++17  
- **Editor:** Visual Studio Code  
- **Compiler:** MinGW-w64 (Windows) with `g++`  
- **External Tools:** FFmpeg for video processing  
- **Other Languages:** Python 3 for authentication (`user_auth.py`)  
- **Cloud DB:** MongoDB Atlas (NoSQL)

## Prerequisites

Ensure the following are installed and configured:

- ✅ **FFmpeg** – Must be in your system's `PATH`.  
- ✅ **C++17 Compiler** – Such as `g++` (MinGW-w64 or similar).  
- ✅ **Python 3** – Required for user login/registration.  
- ✅ **Python packages:**  
  ```bash
  pip install pymongo python-dotenv
  ```
- ✅ **MongoDB Atlas** – Create a free cluster and connection string.

## How to Run

1. **Clone the Project**
   ```bash
   git clone https://github.com/yourname/cpp-video-clipper.git
   cd cpp-video-clipper
   ```

2. **Create a `.env` File** (same folder as `user_auth.py`)
   ```ini
   MONGO_URI=your_mongo_connection_string
   ```

3. **Compile the C++ App**
   ```bash
   g++ clipper.cpp -o video_clipper -std=c++17 -lstdc++fs
   ```

4. **Run the App**
   ```bash
   ./video_clipper
   ```

   You will be prompted to log in or register using the cloud database.

   Once authenticated, the clipper will process the list of clips and save the output files.

## Sample Output Directory Structure

```
/ClippedVideos/
├── Animotica_19_5_0_44_46_clips/
│   ├── 1_Short_Test_Clip_2.mp4
│   └── 2_Short_Test_Clip_3.mp4
```

## Useful Websites

- [cppreference](https://en.cppreference.com/w/) - Comprehensive C++ language reference.  
- [Learn C++](https://www.learncpp.com/) - A great tutorial site for C++.  
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) - Official documentation for FFmpeg commands.  
- [MongoDB Atlas](https://www.mongodb.com/products/platform/atlas-database) - Free cloud database cluster hosting.  
- [python-dotenv](https://pypi.org/project/python-dotenv/) - For managing environment variables in Python.  
- [pymongo Documentation](https://pymongo.readthedocs.io/en/stable/) - MongoDB driver for Python.
