# C++ Video Clipper (Module 1: Language - C++)

## Overview

As a software engineer, I am focused on mastering the foundational building blocks of programming, specifically the C++ language. This initial project involves creating a command-line application to demonstrate my understanding of core C++ concepts and how to interact with external tools.

The software is a console application that acts as a video clipper. It takes a specified input video file and a predefined list of clip segments (defined by start time, end time, and a base name). For each segment, it extracts a new video clip. These clips are saved into a dedicated subfolder, named after the original video, within a user-defined output directory. Each output clip is automatically numbered sequentially (e.g., `1_MyClipName.mp4`).

The application leverages the powerful FFmpeg command-line tool to perform the actual video cutting. It is configured to directly copy video and audio streams (`-c:v copy -c:a copy`) without re-encoding, ensuring maximum speed and preserving original quality. Real-time FFmpeg output is streamed to the console to provide live progress updates.

The purpose of this software is to verify my C++ development environment and to demonstrate proficiency in fundamental C++ programming constructs, file system interactions, and external process execution. This project serves as the foundational "clipper" component for a larger video management and YouTube upload application that will be developed in subsequent modules.

## Unique Module Requirements Met

This software demonstrates the following requirements for the C++ Language module:

- **Variables, Expressions, Conditionals, Loops, Functions, Classes:** These core C++ concepts are integrated throughout the application, particularly within the `VideoClipper` class and its methods, and supporting helper functions.
- **Data structure from STL:** The `std::vector<VideoClipper::ClipInfo>` is used to manage the list of video segments to be extracted. `std::string` and `std::stringstream` are also extensively used.
- **Read and write to a file:** The program creates output directories (`std::filesystem::create_directories`) and writes new video files to disk by executing FFmpeg.
- **Use the `new` and `delete` operators to dynamically create objects:** The `main` function explicitly demonstrates dynamic memory allocation by creating a `VideoClipper` object on the heap using `new` and properly deallocating it with `delete`.

[Clipper CPP Video](https://youtu.be/GaZZ1mwws9g)

## Development Environment

I used **Visual Studio Code** as my primary text editor for writing the source code. To compile the code into a runnable program, I used the **g++ compiler**, which is part of the MinGW-w64 toolchain (on Windows). This setup allows me to compile and run the C++ application directly from the integrated terminal.

The programming language used for this project was C++.

## Prerequisites

Before running this application, ensure you have the following installed and configured:

- **FFmpeg:** Download and install FFmpeg. Its executable's directory (e.g., `C:\ffmpeg\bin` on Windows) must be added to the system's PATH environment variable.
- **C++ Compiler:** A C++17 compatible compiler (like g++ from MinGW-w64 on Windows, or g++/clang++ on Linux/macOS) must be installed and accessible from the terminal.
- **Visual Studio Code:** With the Microsoft "C/C++" extension installed.

## How to Run

1. **Save the Code:** Ensure the provided C++ code (which includes the `main()` function and `VideoClipper` class) is saved as `clipper.cpp` in the project folder.
2. **Open in VS Code:** Open the folder containing the `clipper.cpp` file in Visual Studio Code (`File > Open Folder...`).
3. **Update Video Paths:** Open `clipper.cpp` and **modify the `input_video` and `output_base_directory` variables** (around line 180) to point to the actual video file and desired output folder. _ Example: `std::string input_video = "C:/path/to/video.mp4";` _ Example: `std::string output_base_directory = "C:/path/to/save/clips";`
4. **Open Terminal:** In VS Code, open a new Integrated Terminal (`Terminal > New Terminal` or `Ctrl+` `` `).
5. **Compile:** In the terminal, compile the code using g++. Replace `main.cpp` with `clipper.cpp`:
   ```bash
   g++ clipper.cpp -o video_clipper -std=c++17 -lstdc++fs
   ```
6. **Run:** Execute the compiled program:

- **Windows:** `./video_clipper.exe`
- **macOS/Linux:** `./video_clipper`

The program will print real-time FFmpeg output to the console, showing the progress of each clip extraction. New video files will appear in the specified output directory.

## Useful Websites

- [cppreference](https://en.cppreference.com/w/) - Comprehensive C++ language reference.
- [Learn C++](https://www.learncpp.com/) - A great tutorial site for C++.
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) - Official documentation for FFmpeg commands.
