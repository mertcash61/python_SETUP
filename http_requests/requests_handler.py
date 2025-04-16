import requests

class HTTPRequests:
    """HTTP isteklerini yönetmek için sınıf."""

    @staticmethod
    def get_request(url):
        """GET isteği yapma."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Hata durumunda bir istisna fırlatır
            print("GET isteği başarıyla alındı.")
            return response.json()  # JSON formatında veri döndür
        except requests.exceptions.RequestException as e:
            print(f"GET isteği sırasında bir hata oluştu: {e}")
            return None

    @staticmethod
    def post_request(url, data):
        """POST isteği yapma."""
        attempt = 0
        max_attempts = 5  # Maksimum deneme sayısı
        while attempt < max_attempts:
            try:
                response = requests.post(url, json=data)
                response.raise_for_status()  # Hata durumunda bir istisna fırlatır
                print("POST isteği başarıyla gönderildi.")
                return response.json()  # JSON formatında veri döndür
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP hatası: {http_err}")
                return None
            except requests.exceptions.RequestException as e:
                print(f"POST isteği sırasında bir hata oluştu: {e}")
                attempt += 1  # Deneme sayısını artır
                print(f"Yeniden deneme {attempt}/{max_attempts}...")
                if attempt >= max_attempts:
                    print("Maksimum deneme sayısına ulaşıldı.")
                    return None
            else:
                # Yanıtın belirli bir durumu kontrol edilebilir
                if response.status_code == 200:
                    print("Başarılı yanıt alındı.")
                    return response.json()
                elif response.status_code == 201:
                    print("Yeni kaynak başarıyla oluşturuldu.")
                    return response.json()
                else:
                    print(f"Beklenmeyen durum: {response.status_code}")
                    return None
