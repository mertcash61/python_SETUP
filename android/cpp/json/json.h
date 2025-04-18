#ifndef JSON_H
#define JSON_H

#include <frontend/index.html>
#include <frontend/style.css>
#include <include.json>


// JSON veri türü
using JsonValue = std::variant<std::nullptr_t, bool, int, double, std::string, std::map<std::string, JsonValue>, std::vector<JsonValue>>;

class Json {
public:
    // JSON nesnesini oluşturma
    Json() : value(nullptr) {}

    // JSON nesnesine değer ekleme
    void add(const std::string& key, const JsonValue& val) {
        if (value.index() == 4) { // Eğer bir nesne ise
            std::get<4>(value)[key] = val;
        }
    }

    // JSON nesnesini yazdırma
    void print() const {
        printHelper(value);
    }

private:
    JsonValue value;

    // JSON değerini yazdırma yardımcı fonksiyonu
    void printHelper(const JsonValue& val) const {
        std::visit(overloaded {
            [](std::nullptr_t) { std::cout << "null"; },
            [](bool b) { std::cout << (b ? "true" : "false"); },
            [](int i) { std::cout << i; },
            [](double d) { std::cout << d; },
            [](const std::string& s) { std::cout << "\"" << s << "\""; },
            [this](const std::map<std::string, JsonValue>& obj) {
                std::cout << "{";
                for (const auto& [key, value] : obj) {
                    std::cout << "\"" << key << "\": ";
                    printHelper(value);
                    std::cout << ", ";
                }
                std::cout << "}";
            },
            [this](const std::vector<JsonValue>& arr) {
                std::cout << "[";
                for (const auto& item : arr) {
                    printHelper(item);
                    std::cout << ", ";
                }
                std::cout << "]";
            }
        }, val);
    }
};

// Helper for overloaded lambda
struct overloaded {
    template <typename... Ts>
    struct overload : Ts... { using Ts::operator()...; };
    template <typename... Ts>
    overload(Ts...) -> overload<Ts...>;
};

#endif // JSON_H
