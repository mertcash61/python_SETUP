#include "HttpRequestHandler.hpp"
#include <iostream>
#include <sstream>
#include <chrono>
#include <iomanip>

HttpRequestHandler::HttpRequestHandler() {
    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();
    if (!curl) {
        throw std::runtime_error("CURL başlatılamadı");
    }
}

HttpRequestHandler::~HttpRequestHandler() {
    if (curl) {
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
}

size_t HttpRequestHandler::writeCallback(void* contents, size_t size, size_t nmemb, std::string* userp) {
    size_t realsize = size * nmemb;
    userp->append((char*)contents, realsize);
    return realsize;
}

void HttpRequestHandler::logInfo(const std::string& message) {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    std::cout << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S") 
              << " [INFO] " << message << std::endl;
}

void HttpRequestHandler::logError(const std::string& message) {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    std::cerr << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S") 
              << " [ERROR] " << message << std::endl;
}

json HttpRequestHandler::handleRequest(
    const std::string& url,
    const std::function<CURLcode(CURL*, const std::string&)>& requestFunc,
    const std::map<std::string, std::string>& params
) {
    try {
        logInfo("İstek gönderiliyor: " + url);

        std::string responseString;
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &responseString);
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // Parametreleri URL'e ekle
        if (!params.empty()) {
            std::string paramString;
            for (const auto& param : params) {
                if (!paramString.empty()) paramString += "&";
                paramString += param.first + "=" + param.second;
            }
            std::string fullUrl = url + "?" + paramString;
            curl_easy_setopt(curl, CURLOPT_URL, fullUrl.c_str());
        }

        CURLcode res = requestFunc(curl, url);
        if (res != CURLE_OK) {
            throw std::runtime_error("CURL hatası: " + std::string(curl_easy_strerror(res)));
        }

        long http_code = 0;
        curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
        logInfo("İstek başarılı: " + std::to_string(http_code));

        return json::parse(responseString);

    } catch (const std::exception& e) {
        logError(e.what());
        throw;
    }
}

bool HttpRequestHandler::validateResponse(const json& response) {
    if (!response.is_object()) {
        logError("Yanıt verisi JSON nesnesi değil");
        return false;
    }

    if (response.contains("error")) {
        logError("Yanıtta hata var: " + response["error"].get<std::string>());
        return false;
    }

    return true;
} 