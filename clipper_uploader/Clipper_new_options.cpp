// main.cpp - Updated for Interactive Video Selection and Custom Timestamps

#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <sstream>
#include <array>
#include <cstdio>
#include <cstdlib>

namespace fs = std::filesystem;

long long timeToSeconds(const std::string& time_str) {
    int h = 0, m = 0, s = 0;
    if (sscanf(time_str.c_str(), "%d:%d:%d", &h, &m, &s) != 3) return 0;
    return h * 3600 + m * 60 + s;
}

std::string sanitizeFilename(std::string filename) {
    std::string sanitized_name = "";
    for (char c : filename) {
        if (c == '<' || c == '>' || c == ':' || c == '"' || c == '/' ||
            c == '\\' || c == '|' || c == '?' || c == '*') {
            sanitized_name += '_';
        } else {
            sanitized_name += c;
        }
    }
    return sanitized_name;
}

class VideoClipper {
public:
    struct ClipInfo {
        std::string start_time, end_time, clip_base_name;
        ClipInfo(std::string start, std::string end, std::string name)
            : start_time(std::move(start)), end_time(std::move(end)), clip_base_name(std::move(name)) {}
    };

    VideoClipper(const std::string& input, const std::string& output)
        : input_video_path_(input), base_output_dir_(output) {}

    bool extractClips(const std::vector<ClipInfo>& clips) {
        std::string input_video_base = fs::path(input_video_path_).stem().string();
        fs::path output_path = fs::path(base_output_dir_) / (input_video_base + "_clips");
        if (!fs::exists(output_path)) fs::create_directories(output_path);

        int index = 1;
        for (const auto& clip : clips) {
            long long start_sec = timeToSeconds(clip.start_time);
            long long end_sec = timeToSeconds(clip.end_time);
            long long duration_sec = end_sec - start_sec;
            if (duration_sec <= 0) continue;

            std::stringstream cmd;
            std::string output_name = std::to_string(index) + "_" + sanitizeFilename(clip.clip_base_name) + ".mp4";
            std::string output_full_path = (output_path / output_name).string();
            cmd << "ffmpeg -y -ss " << clip.start_time << " -i \"" << input_video_path_ << "\" -t "
                << duration_sec << " -c:v copy -c:a copy -movflags +faststart \"" << output_full_path << "\" 2>&1";

            std::cout << "Processing: " << clip.clip_base_name << std::endl;
            FILE* pipe = _popen(cmd.str().c_str(), "r");
            if (!pipe) continue;
            std::array<char, 128> buffer;
            while (fgets(buffer.data(), buffer.size(), pipe) != nullptr) {
                std::cout << buffer.data();
            }
            _pclose(pipe);
            ++index;
        }
        return true;
    }

private:
    std::string input_video_path_;
    std::string base_output_dir_;
};

int main() {
    std::cout << "🔐 Launching login system...\n";
    int auth_result = system("python user_auth\\mysql\\mysql_user_auth.py");
    if (auth_result != 0) {
        std::cout << "👋 Exiting app.\n";
        return 0;
    }
    std::cout << "✅ Authenticated!\n";

    std::string input_video, output_dir;
    std::cout << "Enter input video file path: ";
    std::getline(std::cin, input_video);
    std::cout << "Enter output directory: ";
    std::getline(std::cin, output_dir);

    int mode;
    std::cout << "Select mode: 1 for Manual, 2 for Automatic: ";
    std::cin >> mode;
    std::cin.ignore();

    std::vector<VideoClipper::ClipInfo> clips;

    if (mode == 1) {
        while (true) {
            std::string start, end;
            std::cout << "Enter start time (HH:MM:SS): ";
            std::getline(std::cin, start);
            std::cout << "Enter end time (HH:MM:SS): ";
            std::getline(std::cin, end);
            std::string name = "ManualClip_" + start + "_to_" + end;
            clips.emplace_back(start, end, name);

            int cont;
            std::cout << "Add another timestamp? (1 = Yes, 2 = No): ";
            std::cin >> cont;
            std::cin.ignore();
            if (cont != 1) break;
        }
    } else if (mode == 2) {
        int interval;
        std::cout << "Select interval in minutes (1, 2, 3, 5, 10, 15, 20): ";
        std::cin >> interval;
        std::cin.ignore();

        // Determine total video duration using ffprobe
        std::stringstream probe_cmd;
        probe_cmd << "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"" << input_video << "\"";
        FILE* probe = _popen(probe_cmd.str().c_str(), "r");
        char buf[64];
        fgets(buf, sizeof(buf), probe);
        double total_seconds = atof(buf);
        _pclose(probe);

        for (int start = 0, i = 1; start < static_cast<int>(total_seconds); start += interval * 60, ++i) {
            int end = std::min(start + interval * 60, static_cast<int>(total_seconds));
            int sh = start / 3600, sm = (start % 3600) / 60, ss = start % 60;
            int eh = end / 3600, em = (end % 3600) / 60, es = end % 60;

            char start_buf[16], end_buf[16];
            sprintf(start_buf, "%02d:%02d:%02d", sh, sm, ss);
            sprintf(end_buf, "%02d:%02d:%02d", eh, em, es);

            std::string name = "AutoClip_" + std::to_string(i);
            clips.emplace_back(start_buf, end_buf, name);
        }
    } else {
        std::cout << "Invalid mode selected. Exiting.\n";
        return 1;
    }

    std::cout << "Start processing? (1 = Yes, 2 = No): ";
    int confirm;
    std::cin >> confirm;
    if (confirm != 1) return 0;

    VideoClipper* clipper = new VideoClipper(input_video, output_dir);
    clipper->extractClips(clips);
    delete clipper;

    std::cout << "\nAll done! Press Enter to exit." << std::endl;
    std::cin.ignore();
    std::cin.get();
    return 0;
}