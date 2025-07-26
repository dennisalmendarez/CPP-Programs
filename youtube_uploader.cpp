#include <iostream>
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>
#include <nlohmann/json.hpp> // For JSON handling

namespace fs = std::filesystem;
using json = nlohmann::json;

struct VideoMeta {
    std::string file;
    std::string title;
    std::string description;
    std::string hashtags;
    std::string tags_csv;
    std::string language;
};

std::string ask(const std::string& prompt, const std::string& default_value = "") {
    std::string input;
    std::cout << prompt << (default_value.empty() ? "" : " (Enter to reuse: " + default_value + ")") << "\n> ";
    std::getline(std::cin, input);
    return input.empty() ? default_value : input;
}

int main() {
    std::cout << "🔐 Launching login system...\n";
    int auth_result = system("python user_auth.py");
    if (auth_result != 0) {
        std::cout << "👋 Exiting app.\n";
        return 0;
    }
    std::cout << "✅ Authenticated!\n";

    std::string folder_path;
    std::cout << "📁 Enter path to video folder: ";
    std::getline(std::cin, folder_path);

    if (!fs::exists(folder_path) || !fs::is_directory(folder_path)) {
        std::cerr << "❌ Invalid folder.\n";
        return 1;
    }

    std::vector<VideoMeta> video_inputs;
    std::string last_title, last_desc, last_tags, last_hashtags, last_lang;

    for (const auto& file : fs::directory_iterator(folder_path)) {
        if (file.path().extension() == ".mp4") {
            std::cout << "\n🎬 Video: " << file.path().filename().string() << "\n";
            VideoMeta meta;
            meta.file = file.path().filename().string();
            meta.title = ask("Enter title", last_title);
            meta.description = ask("Enter description", last_desc);
            meta.hashtags = ask("Enter hashtags", last_hashtags);
            meta.tags_csv = ask("Enter tags (comma separated)", last_tags);
            meta.language = ask("Enter language (e.g., en, es)", last_lang);

            // Store last inputs
            last_title = meta.title;
            last_desc = meta.description;
            last_hashtags = meta.hashtags;
            last_tags = meta.tags_csv;
            last_lang = meta.language;

            video_inputs.push_back(meta);
        }
    }

    // Convert to JSON
    json j;
    for (const auto& v : video_inputs) {
        j.push_back({
            {"file", v.file},
            {"title", v.title},
            {"description", v.description},
            {"hashtags", v.hashtags},
            {"tags", v.tags_csv},
            {"language", v.language}
        });
    }

    // Save JSON metadata
    std::string json_path = "video_upload_metadata.json";
    std::ofstream out(json_path);
    out << j.dump(4);
    out.close();

    // Call Python uploader
    std::string command = "python youtube_uploader.py \"" + folder_path + "\" \"" + json_path + "\"";
    std::cout << "\n🚀 Starting upload...\n";
    int result = system(command.c_str());

    if (result == 0)
        std::cout << "✅ Upload completed.\n";
    else
        std::cerr << "❌ Upload failed.\n";

    return 0;
}
