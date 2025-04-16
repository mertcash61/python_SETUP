#include <cstdio>  // Standart girdi/çıktı işlemleri için
#include <json/json.h>  // JSON işleme kütüphanesi

#include <curl/curl.h>

// JSON formatında veri göndermek için bir fonksiyon
void sendJsonData(const std::string& jsonData) {
    CURL* curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.example.com/save_results");  // Gerçek URL ile değiştirin
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonData.c_str());  // JSON verisini gönder

        // Başlıkları ayarlama
        struct curl_slist* headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // İsteği gönderme
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }

        // Temizlik
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
}

int main() {
    std::cout << "C++ Android Uygulaması" << std::endl;

    // Örnek JSON verisi
    std::string jsonData = R"({"slope": 1.5, "intercept": 0.5})";  // Örnek regresyon sonuçları

    // JSON verisini gönder
    sendJsonData(jsonData);

    return 0;
}
