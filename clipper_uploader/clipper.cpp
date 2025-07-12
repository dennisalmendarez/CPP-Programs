// main.cpp
// This is the main file for Module 1: C++ Language.
// It implements a command-line video clipping tool using C++ and FFmpeg.
// This application demonstrates core C++ concepts, STL data structures,
// file system interactions, and executing external commands.

#include <iostream>     // For standard input/output (console)
#include <string>       // For std::string manipulation
#include <vector>       // For std::vector (STL data structure)
#include <algorithm>    // For std::sort, if needed for future features (not strictly used here)
#include <filesystem>   // C++17 for file system operations (creating directories, checking paths)
#include <chrono>       // For time calculations, if needed for future timing
#include <cstdlib>      // For system() call (will be replaced by _popen)
#include <sstream>      // For constructing command strings dynamically
#include <cstdio>       // For sscanf, _popen, _pclose
#include <array>        // For std::array (buffer for _popen output)

// Unique Module Requirements:
// 1 Variables, Expressions, Conditionals, Loops, Functions, Classes (demonstrated throughout)
// 2 Data structure from STL (std::vector for ClipInfo, std::array for _popen buffer)
// 3 Read and write to a file (output video files via FFmpeg)
// 4 Use the new and delete operators to dynamically create objects (demonstrated in main)

// Namespace for easier access to filesystem functions
namespace fs = std::filesystem;

// --- Helper Functions ---

// Tuesday's work: Implemented helper function timeToSeconds()
/**
 * @brief Converts a time string (HH:MM:SS) into total seconds.
 * @param time_str The time string in "HH:MM:SS" format.
 * @return Total number of seconds.
 */
long long timeToSeconds(const std::string& time_str) {
    int h = 0, m = 0, s = 0;
    // Using sscanf to parse the string into integers
    // Note: For more robust error handling in production, consider parsing manually or regex.
    if (sscanf(time_str.c_str(), "%d:%d:%d", &h, &m, &s) != 3) {
        std::cerr << "Warning: Invalid time format for '" << time_str << "'. Assuming 00:00:00." << std::endl;
        return 0;
    }
    return h * 3600 + m * 60 + s;
}

// Tuesday's work: Implemented helper function sanitizeFilename()
/**
 * @brief Sanitizes a filename string to remove characters problematic for file systems.
 * Specifically targets Windows forbidden characters and replaces them with underscores.
 * @param filename The original filename string.
 * @return A sanitized filename string.
 */
std::string sanitizeFilename(std::string filename) {
    std::string sanitized_name = "";
    for (char c : filename) {
        // List of characters generally problematic in Windows filenames: < > : " / \ | ? *
        // Unix/Linux primarily restricts '/'
        if (c == '<' || c == '>' || c == ':' || c == '"' || c == '/' ||
            c == '\\' || c == '|' || c == '?' || c == '*') {
            sanitized_name += '_'; // Replace with underscore
        }
        else {
            sanitized_name += c;
        }
    }
    return sanitized_name;
}

// --- VideoClipper Class (Demonstrates Classes, Variables, Functions) ---

/**
 * @brief The VideoClipper class handles the logic for extracting video clips using FFmpeg.
 * It encapsulates the input video path and provides functionality to process a list of clips.
 */
class VideoClipper {
    public:
        // Tuesday's work: Defined ClipInfo struct
        /**
         * @brief Structure to hold information for a single video clip to be extracted.
         * This demonstrates a user-defined structure.
         */
        struct ClipInfo {
            std::string start_time;         // Start timestamp (HH:MM:SS)
            std::string end_time;           // End timestamp (HH:MM:SS)
            std::string clip_base_name;     // Base name provided by the user (e.g., "Short_Test_Clip")

            // Constructor for ClipInfo
            ClipInfo(std::string start, std::string end, std::string name)
                : start_time(std::move(start)), end_time(std::move(end)), clip_base_name(std::move(name)) {}
        };

        // Wednesday's work: Implemented VideoClipper constructor
        /**
         * @brief Constructor for the VideoClipper.
         * @param input_video_path The full path to the input video file.
         * @param base_output_dir The base directory where all processed videos will be stored.
         */
        VideoClipper(const std::string& input_video_path, const std::string& base_output_dir)
            : input_video_path_(input_video_path), base_output_dir_(base_output_dir) {
            // Conditional check: Verify if the input video exists
            if (!fs::exists(input_video_path_)) {
                std::cerr << "Error: Input video file not found at '" << input_video_path_ << "'" << std::endl;
                // In a real application, might throw an exception or set an error state.
            }
            else {
                std::cout << "VideoClipper initialized for input: '" << input_video_path_ << "'" << std::endl;
            }
        }

        /**
         * @brief Extracts a series of video clips based on the provided ClipInfo vector.
         * This function demonstrates loops and complex logic within a method.
         * Now uses _popen to capture FFmpeg's real-time output.
         * @param clips_to_extract A std::vector of ClipInfo objects, detailing each clip.
         * @return true if all clips were attempted to be extracted (even if some failed), false if
         * there was a critical error like failing to create the output directory.
         */
        bool extractClips(const std::vector<ClipInfo>& clips_to_extract) {
            if (clips_to_extract.empty()) {
                std::cout << "No clips specified for extraction." << std::endl;
                return true; // No work to do, so considered successful
            }

            // Extract the base name of the input video (e.g., "Animotica_19_5_0_44_46")
            // This is an expression involving filesystem operations.
            std::string input_video_base_name = fs::path(input_video_path_).stem().string();

            // Wednesday's work: Implemented directory creation logic
            // Construct the specific output directory for this set of clips
            // Example: VideoProcessorOutput/Animotica_19_5_0_44_46_clips
            fs::path clip_output_path = fs::path(base_output_dir_) / (input_video_base_name + "_clips");
            std::string clip_output_dir_str = clip_output_path.string();

            // Conditional check: Create the output directory if it doesn't exist
            if (!fs::exists(clip_output_path)) {
                if (!fs::create_directories(clip_output_path)) {
                    std::cerr << "❌ Error: Could not create output directory: '" << clip_output_dir_str << "'" << std::endl;
                    return false; // Critical failure
                }
                std::cout << "Created output directory: '" << clip_output_dir_str << "'" << std::endl;
            }
            else {
                std::cout << "Output directory already exists: '" << clip_output_dir_str << "'" << std::endl;
            }

            bool all_clips_processed_successfully = true;
            int clip_sequence_number = 1; // Variable for numbering clips

            // Thursday's work: Implemented the loop for processing clips
            // Loop through each clip configuration provided
            for (const auto& clip : clips_to_extract) {
                // Construct the output filename using the new convention: [number]_[user_base_name].mp4
                std::string output_filename_base = std::to_string(clip_sequence_number) + "_" + sanitizeFilename(clip.clip_base_name);
                std::string output_clip_path = (clip_output_path / (output_filename_base + ".mp4")).string();

                // Calculate duration of the clip in seconds
                long long start_sec = timeToSeconds(clip.start_time);
                long long end_sec = timeToSeconds(clip.end_time);
                long long duration_sec = end_sec - start_sec;

                // Conditional check: Ensure valid duration
                if (duration_sec <= 0) {
                    std::cerr << "❌ Error: Invalid duration for clip '" << clip.clip_base_name
                            << "' (Start: " << clip.start_time << ", End: " << clip.end_time
                            << "). End time must be after start time. Skipping this clip." << std::endl;
                    all_clips_processed_successfully = false;
                    clip_sequence_number++;
                    continue; // Move to the next clip
                }

                // Wednesday's work: Began constructing FFmpeg command string
                // Thursday's work: Completed FFmpeg command string construction
                // Construct the FFmpeg command string
                std::stringstream command_stream;
                command_stream << "ffmpeg -y " // -y to overwrite output files without asking
                            << "-ss " << clip.start_time << " " // Seek to start time
                            << "-i \"" << input_video_path_ << "\" " // Input file
                            << "-t " << duration_sec << " " // Duration of the output clip
                            << "-c:v copy -c:a copy " // Copy video and audio streams (no re-encoding for speed)
                            << "-movflags +faststart " // Optimize for web playback
                            << "\"" << output_clip_path << "\" 2>&1"; // Redirect stderr to stdout for _popen

                std::string command = command_stream.str();

                std::cout << "\n🎬 Extracting clip (" << clip_sequence_number << "/" << clips_to_extract.size() << "): "
                        << clip.clip_base_name << " from " << clip.start_time << " to " << clip.end_time << "..." << std::endl;
                std::cout << "  Command: " << command << std::endl;
                std::cout << "  FFmpeg Output (real-time):" << std::endl;

                // Thursday's work: Implemented _popen to execute FFmpeg and capture output
                // Execute the FFmpeg command using _popen and capture its output
                // _popen is for Windows; for Linux/macOS, use popen
                FILE* pipe = _popen(command.c_str(), "r"); // "r" for read mode
                if (!pipe) {
                    std::cerr << "❌ Error: Could not open pipe to FFmpeg. Command: " << command << std::endl;
                    all_clips_processed_successfully = false;
                    clip_sequence_number++;
                    continue;
                }

                std::array<char, 128> buffer; // Small buffer for reading output line by line
                std::string result_output;
                while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
                    result_output += buffer.data();
                    // Print FFmpeg's output directly to console for real-time feedback
                    std::cout << buffer.data();
                }

                int result_code = _pclose(pipe); // Close the pipe and get FFmpeg's exit code

                // Thursday's work: Implemented conditional check for FFmpeg result
                // Conditional check: Report success or failure
                if (result_code == 0) {
                    std::cout << "\n✅ Successfully saved: '" << output_clip_path << "'" << std::endl;
                }
                else {
                    // Friday's work: Added more robust error messages
                    std::cerr << "\n❌ Error extracting clip '" << clip.clip_base_name
                            << "'. FFmpeg command failed with exit code: " << result_code << std::endl;
                    std::cerr << "FFmpeg Full Output:\n" << result_output << std::endl; // Print full captured output on error
                    all_clips_processed_successfully = false;
                }
                clip_sequence_number++;
            }

            if (all_clips_processed_successfully) {
                std::cout << "\n✅ All specified clips have been processed successfully." << std::endl;
            }
            else {
                std::cout << "\n⚠️ Some clips failed to process. Check error messages above." << std::endl;
            }
            return all_clips_processed_successfully;
        }

    private:
        std::string input_video_path_;  // Private variable to store the input video path
        std::string base_output_dir_;   // Private variable for the base output directory
    };


// --- Main Application Entry Point ---

int main() {
    // Monday's work: Initial main function structure and includes
    std::cout << "--- CSE 310: C++ Video Clipper (Module 1 - Console App) ---" << std::endl;
    std::cout << "This application demonstrates C++ fundamentals by clipping videos." << std::endl;
    std::cout << "Ensure FFmpeg is installed and accessible in your system's PATH." << std::endl;
    std::cout << "---------------------------------------------------------" << std::endl << std::endl;

    // --- Configuration for this run (hardcoded for Module 1) ---
    // Use forward slashes or double backslashes for Windows paths.
    std::string input_video = "F:/2025-05-20 11-27-18.mkv"; // Input video file path

    // Base directory for all processed video outputs
    std::string output_base_directory = "f:/ClippedVideos"; // Output directory for C++
    // std::string output_base_directory = "./ProcessedVideos"; // Relative path (current directory)

    // Wednesday's work: Added base output directory creation
    // Ensuring the base output directory exists
    if (!fs::exists(output_base_directory)) {
        try {
            fs::create_directories(output_base_directory);
            std::cout << "Created base output directory: '" << output_base_directory << "'" << std::endl;
        } catch (const fs::filesystem_error& e) {
            std::cerr << "❌ Error: Could not create base output directory '" << output_base_directory << "': " << e.what() << std::endl;
            std::cerr << "Please ensure you have write permissions to this location." << std::endl;
            // In a console app, you might exit here if the base directory is critical.
            return 1; // Indicate error
        }
    }


    // List of clips to extract.
    // In later modules, this would come from user input via a GUI or a configuration file.
    std::vector<VideoClipper::ClipInfo> my_clips = {
        {"00:00:00", "00:03:01", "Short_Test_Clip_2"}, // Added a short test clip for quicker feedback
        {"00:03:01", "00:06:02", "Short_Test_Clip_3"},
        };

    // --- Dynamic Memory Allocation Example (Module 1 Requirement) ---
    // Monday's work: Basic structure for dynamic allocation (will be fully implemented later)
    // Creating an object on the heap using 'new'.
    std::cout << "\nDemonstrating dynamic memory allocation for VideoClipper..." << std::endl;
    VideoClipper* clipper_ptr = nullptr; // Initialize pointer to nullptr
    try {
        // Allocate a VideoClipper object on the heap
        clipper_ptr = new VideoClipper(input_video, output_base_directory);
        std::cout << "VideoClipper object successfully allocated on the heap." << std::endl;

        // Perform the clipping operations using the dynamically allocated object
        bool success = clipper_ptr->extractClips(my_clips);
        if (success) {
            std::cout << "\n✅ All valid clips processed by the dynamically allocated clipper." << std::endl;
        }
        else {
            std::cout << "\n⚠️ Some clips failed to process. Check console output for details." << std::endl;
        }
    } catch (const std::bad_alloc& e) {
        // Catch block for memory allocation failures
        std::cerr << "❌ Memory allocation failed: " << e.what() << std::endl;
        return 1; // Indicate error
    }

    // Deallocating the object from the heap using 'delete'.
    // This is crucial to prevent memory leaks when using 'new'.
    if (clipper_ptr != nullptr) {
        delete clipper_ptr; // Deallocate the memory
        clipper_ptr = nullptr; // Set the pointer to null after deletion to avoid dangling pointers
        std::cout << "VideoClipper object successfully deallocated from the heap." << std::endl;
    }
    // --- End Dynamic Memory Allocation Example ---

    std::cout << "\n--- Module 1: C++ Video Clipper (End) ---" << std::endl;
    std::cout << "Press Enter to exit." << std::endl;
    std::cin.get(); // Keep console open until user presses Enter

    return 0; // Indicate successful execution
}