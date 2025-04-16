import requests

class RequestsHandler:
    """HTTP isteklerini yönetmek için sınıf."""

    @staticmethod
    def get_request(url):
        """GET isteği yapma."""
        response = requests.get(url)
        if response.status_code == 200:
            print("GET isteği başarıyla alındı.")
            return response.json()  # JSON formatında veri döndür
        else:
            print("GET isteği sırasında bir hata oluştu.")
            return None

    @staticmethod
    def post_request(url, data):
        """POST isteği yapma."""
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("POST isteği başarıyla gönderildi.")
            return response.json()  # JSON formatında veri döndür
        else:
            print("POST isteği sırasında bir hata oluştu.")
            return None
