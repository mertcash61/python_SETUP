import requests
from typing import Dict, Any, Callable, Optional
import logging
from requests.exceptions import RequestException

class RequestsHandler:
    """
    HTTP isteklerini işleyen yardımcı sınıf.
    """
    
    def __init__(self):
        """
        RequestsHandler sınıfı başlatıcısı
        """
        # Loglama ayarları
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def handle_request(
        self,
        request_func: Callable,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        HTTP isteğini işler ve yanıtı döndürür
        
        Args:
            request_func (Callable): İstek fonksiyonu (get, post, put, delete)
            url (str): İstek URL'i
            **kwargs: İstek parametreleri
            
        Returns:
            Dict[str, Any]: Yanıt verisi
            
        Raises:
            RequestException: İstek başarısız olduğunda
        """
        try:
            self.logger.info(f"İstek gönderiliyor: {url}")
            response = request_func(url, **kwargs)
            response.raise_for_status()
            
            self.logger.info(f"İstek başarılı: {response.status_code}")
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP hatası: {e}")
            raise RequestException(f"HTTP hatası: {e}")
            
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Bağlantı hatası: {e}")
            raise RequestException(f"Bağlantı hatası: {e}")
            
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Zaman aşımı: {e}")
            raise RequestException(f"Zaman aşımı: {e}")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"İstek hatası: {e}")
            raise RequestException(f"İstek hatası: {e}")
            
        except Exception as e:
            self.logger.error(f"Beklenmeyen hata: {e}")
            raise RequestException(f"Beklenmeyen hata: {e}")
            
    def validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Yanıt verisini doğrular
        
        Args:
            response (Dict[str, Any]): Doğrulanacak yanıt
            
        Returns:
            bool: Doğrulama başarılı ise True
        """
        if not isinstance(response, dict):
            self.logger.error("Yanıt verisi sözlük tipinde değil")
            return False
            
        if 'error' in response:
            self.logger.error(f"Yanıtta hata var: {response['error']}")
            return False
            
        return True
