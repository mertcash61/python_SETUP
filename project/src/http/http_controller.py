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
        try:
            # Endpoint'i temel URL ile birleştir
            full_url = self._build_url(endpoint)
            self.logger.info(f"GET isteği gönderiliyor: {full_url}")
            
            response = self.session.get(
                full_url,
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            self.logger.info(f"GET isteği başarılı: {response.status_code}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET isteği başarısız: {str(e)}")
            raise
        
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        POST isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Optional[Dict[str, Any]]): Gönderilecek veri
            
        Returns:
            Dict[str, Any]: Yanıt verisi
        """
        try:
            # Endpoint'i temel URL ile birleştir
            full_url = self._build_url(endpoint)
            self.logger.info(f"POST isteği gönderiliyor: {full_url}")
            
            response = self.session.post(
                full_url,
                json=data,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            self.logger.info(f"POST isteği başarılı: {response.status_code}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST isteği başarısız: {str(e)}")
            raise
        
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
        try:
            url = self._build_url(endpoint)
            self.logger.info(f"DELETE isteği gönderiliyor: {url}")
            
            response = self.session.delete(
                url,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            self.logger.info(f"DELETE isteği başarılı: {response.status_code}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE isteği başarısız: {str(e)}")
            raise
        
    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        İstek başlıklarını ayarlar
        
        Args:
            headers (Dict[str, str]): Başlık bilgileri
        """
        try:
            self.session.headers.update(headers)
            self.logger.info(f"Başlıklar güncellendi: {headers}")
        except Exception as e:
            self.logger.error(f"Başlık güncelleme hatası: {str(e)}")
            raise
        
    def clear_headers(self) -> None:
        """
        Tüm istek başlıklarını temizler
        """
        try:
            self.session.headers.clear()
            self.logger.info("Tüm başlıklar temizlendi")
        except Exception as e:
            self.logger.error(f"Başlık temizleme hatası: {str(e)}")
            raise
        
    def close(self) -> None:
        """
        HTTP oturumunu kapatır
        """
        try:
            if self.session:
                self.session.close()
                self.logger.info("HTTP oturumu kapatıldı")
        except Exception as e:
            self.logger.error(f"Oturum kapatma hatası: {str(e)}")
            raise
