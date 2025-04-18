import requests
from typing import Dict, Any, Optional
import logging
from .requests_handler import RequestsHandler

class HTTPController:
    """
    HTTP isteklerini yöneten ana sınıf.
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        HTTPController sınıfı başlatıcısı
        
        Args:
            base_url (str): API'nin temel URL'i
            timeout (int): İstek zaman aşımı süresi (saniye)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.requests_handler = RequestsHandler()
        
        # Loglama ayarları
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def _build_url(self, endpoint: str) -> str:
        """
        Endpoint'i temel URL ile birleştirir
        
        Args:
            endpoint (str): API endpoint'i
            
        Returns:
            str: Tam URL
        """
        return f"{self.base_url}/{endpoint.lstrip('/')}"
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GET isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            params (Optional[Dict[str, Any]]): İstek parametreleri
            
        Returns:
            Dict[str, Any]: Yanıt verisi
        """
        url = self._build_url(endpoint)
        return self.requests_handler.handle_request(
            self.session.get,
            url,
            params=params,
            timeout=self.timeout
        )
        
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        POST isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Optional[Dict[str, Any]]): Gönderilecek veri
            
        Returns:
            Dict[str, Any]: Yanıt verisi
        """
        url = self._build_url(endpoint)
        return self.requests_handler.handle_request(
            self.session.post,
            url,
            json=data,
            timeout=self.timeout
        )
        
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        PUT isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Optional[Dict[str, Any]]): Gönderilecek veri
            
        Returns:
            Dict[str, Any]: Yanıt verisi
        """
        url = self._build_url(endpoint)
        return self.requests_handler.handle_request(
            self.session.put,
            url,
            json=data,
            timeout=self.timeout
        )
        
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        DELETE isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            
        Returns:
            Dict[str, Any]: Yanıt verisi
        """
        url = self._build_url(endpoint)
        return self.requests_handler.handle_request(
            self.session.delete,
            url,
            timeout=self.timeout
        )
        
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        İstek başlıklarını ayarlar
        
        Args:
            headers (Dict[str, str]): Başlık bilgileri
        """
        self.session.headers.update(headers)
        
    def clear_headers(self) -> None:
        """
        Tüm istek başlıklarını temizler
        """
        self.session.headers.clear()
        
    def close(self) -> None:
        """
        HTTP oturumunu kapatır
        """
        self.session.close()
