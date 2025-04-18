#pragma once

#include <string>
#include <map>
#include <vector>
#include <variant>
#include <stdexcept>

namespace nlohmann {

class json {
public:
    using value_t = std::variant<
        std::nullptr_t,
        bool,
        int64_t,
        double,
        std::string,
        std::vector<json>,
        std::map<std::string, json>
    >;

    json() : m_value(nullptr) {}
    json(const char* str) : m_value(std::string(str)) {}
    json(const std::string& str) : m_value(str) {}
    json(int64_t val) : m_value(val) {}
    json(double val) : m_value(val) {}
    json(bool val) : m_value(val) {}

    bool is_object() const {
        return std::holds_alternative<std::map<std::string, json>>(m_value);
    }

    bool contains(const std::string& key) const {
        if (!is_object()) return false;
        const auto& obj = std::get<std::map<std::string, json>>(m_value);
        return obj.find(key) != obj.end();
    }

    template<typename T>
    T get() const {
        try {
            return std::get<T>(m_value);
        } catch (const std::bad_variant_access&) {
            throw std::runtime_error("JSON değeri istenen tipte değil");
        }
    }

    static json parse(const std::string& str) {
        // Basit JSON ayrıştırma (gerçek uygulamada daha kapsamlı olmalı)
        if (str == "null") return json();
        if (str == "true") return json(true);
        if (str == "false") return json(false);
        if (str.front() == '"' && str.back() == '"') {
            return json(str.substr(1, str.length() - 2));
        }
        try {
            return json(std::stoll(str));
        } catch (...) {
            try {
                return json(std::stod(str));
            } catch (...) {
                throw std::runtime_error("Geçersiz JSON formatı");
            }
        }
    }

private:
    value_t m_value;
};

} // namespace nlohmann
