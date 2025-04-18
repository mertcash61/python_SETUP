import requests
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import logging

class HTTPController:
    """
    Setup uygulaması için HTTP isteklerini yöneten controller sınıfı.
    
    Bu sınıf, HTTP isteklerini göndermek ve yönetmek için gerekli tüm metodları içerir.
    Otomatik yeniden deneme, timeout yönetimi ve hata yakalama özelliklerine sahiptir.
    """
    
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
        verify_ssl: bool = True
    ) -> None:
        """
        HTTP Controller sınıfı başlatıcısı
        
        Args:
            base_url (str): API'nin temel URL'i
            headers (Dict[str, str], optional): Varsayılan HTTP başlıkları
            timeout (int): İstek zaman aşımı süresi (saniye)
            max_retries (int): Maksimum yeniden deneme sayısı
            retry_delay (int): Yeniden denemeler arası bekleme süresi (saniye)
            verify_ssl (bool): SSL sertifika doğrulaması yapılsın mı
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.verify_ssl = verify_ssl
        
        # Session oluşturma ve retry stratejisi
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=retry_delay,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        if self.headers:
            self.session.headers.update(self.headers)
            
        # SSL doğrulama ayarı
        self.session.verify = verify_ssl
        
        # Loglama ayarları
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _build_url(self, endpoint: str) -> str:
        """
        Endpoint'i base URL ile birleştirir
        
        Args:
            endpoint (str): API endpoint'i
            
        Returns:
            str: Tam URL
        """
        endpoint = endpoint.lstrip('/')
        return urljoin(f"{self.base_url}/", endpoint)

    def _prepare_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        İstek başlıklarını hazırlar
        
        Args:
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            
        Returns:
            Dict[str, str]: Birleştirilmiş HTTP başlıkları
        """
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        return request_headers

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        HTTP isteği gönderir
        
        Args:
            method (str): HTTP metodu (GET, POST, PUT, DELETE, PATCH)
            endpoint (str): API endpoint'i
            **kwargs: İstek parametreleri
            
        Returns:
            requests.Response: HTTP yanıtı
        """
        url = self._build_url(endpoint)
        
        try:
            self.logger.info(f"{method} isteği gönderiliyor: {url}")
            response = getattr(self.session, method.lower())(
                url,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            response.raise_for_status()
            self.logger.info(f"İstek başarılı: {response.status_code}")
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"İstek başarısız: {str(e)}")
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        GET isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            params (Dict[str, Any], optional): URL parametreleri
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            **kwargs: requests.get() için ek parametreler
            
        Returns:
            requests.Response: HTTP yanıtı
        """
        return self._make_request(
            "GET",
            endpoint,
            params=params,
            headers=self._prepare_headers(headers),
            **kwargs
        )

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        POST isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Union[Dict[str, Any], str, bytes], optional): Form verisi
            json (Dict[str, Any], optional): JSON verisi
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            **kwargs: requests.post() için ek parametreler
            
        Returns:
            requests.Response: HTTP yanıtı
        """
        return self._make_request(
            "POST",
            endpoint,
            data=data,
            json=json,
            headers=self._prepare_headers(headers),
            **kwargs
        )

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        PUT isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Dict[str, Any], optional): Form verisi
            json (Dict[str, Any], optional): JSON verisi
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            **kwargs: requests.put() için ek parametreler
            
        Returns:
            requests.Response: HTTP yanıtı
            
        Raises:
            requests.exceptions.RequestException: İstek başarısız olduğunda
        """
        return self._make_request(
            "PUT",
            endpoint,
            data=data,
            json=json,
            headers=self._prepare_headers(headers),
            **kwargs
        )

    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        DELETE isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            **kwargs: requests.delete() için ek parametreler
            
        Returns:
            requests.Response: HTTP yanıtı
            
        Raises:
            requests.exceptions.RequestException: İstek başarısız olduğunda
        """
        return self._make_request(
            "DELETE",
            endpoint,
            headers=self._prepare_headers(headers),
            **kwargs
        )

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        PATCH isteği gönderir
        
        Args:
            endpoint (str): API endpoint'i
            data (Dict[str, Any], optional): Form verisi
            json (Dict[str, Any], optional): JSON verisi
            headers (Dict[str, str], optional): Ek HTTP başlıkları
            **kwargs: requests.patch() için ek parametreler
            
        Returns:
            requests.Response: HTTP yanıtı
            
        Raises:
            requests.exceptions.RequestException: İstek başarısız olduğunda
        """
        return self._make_request(
            "PATCH",
            endpoint,
            data=data,
            json=json,
            headers=self._prepare_headers(headers),
            **kwargs
        )

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        HTTP başlıklarını günceller
        
        Args:
            headers (Dict[str, str]): Yeni HTTP başlıkları
        """
        self.headers.update(headers)
        self.session.headers.update(headers)

    def clear_headers(self) -> None:
        """
        Tüm HTTP başlıklarını temizler
        """
        self.headers.clear()
        self.session.headers.clear()

    def close(self) -> None:
        """
        HTTP oturumunu kapatır
        """
        self.session.close()
        
    def get_json(self, response: requests.Response) -> Dict[str, Any]:
        """
        HTTP yanıtını JSON olarak döndürür
        
        Args:
            response (requests.Response): HTTP yanıtı
            
        Returns:
            Dict[str, Any]: JSON verisi
        """
        return response.json()
        
    def get_text(self, response: requests.Response) -> str:
        """
        HTTP yanıtını metin olarak döndürür
        
        Args:
            response (requests.Response): HTTP yanıtı
            
        Returns:
            str: Yanıt metni
        """
        return response.text
