#pragma once

#include <string>
#include <map>
#include <functional>
#include <memory>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class HttpRequestHandler {
public:
    HttpRequestHandler();
    ~HttpRequestHandler();

    // İstek gönderme fonksiyonu
    json handleRequest(
        const std::string& url,
        const std::function<CURLcode(CURL*, const std::string&)>& requestFunc,
        const std::map<std::string, std::string>& params = {}
    );

    // Yanıt doğrulama fonksiyonu
    bool validateResponse(const json& response);

private:
    // CURL yanıt verisini saklamak için callback fonksiyonu
    static size_t writeCallback(void* contents, size_t size, size_t nmemb, std::string* userp);

    // Loglama fonksiyonları
    void logInfo(const std::string& message);
    void logError(const std::string& message);

    // CURL handle'ı
    CURL* curl;
}; 