from typing import Dict, Any, Optional
from .http_controller import HTTPController
from ..src.auth.auth.controller import AuthController
import logging

class MainController:
    """
    Setup uygulaması için ana HTTP işlemleri ve kullanıcı yönetimi controller sınıfı.
    
    Bu sınıf, HTTP isteklerini ve kullanıcı işlemlerini yönetir.
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None
    ):
        """
        Main Controller sınıfı başlatıcısı
        
        Args:
            base_url (str): API'nin temel URL'i
            api_key (str, optional): API anahtarı
            secret_key (str, optional): JWT imzalama anahtarı
        """
        self.base_url = base_url
        self.api_key = api_key
        
        # Loglama ayarları
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # HTTP Controller oluştur
        headers = {}
        if api_key:
            headers["X-API-Key"] = api_key
            
        self.http = HTTPController(base_url, headers=headers)
        
        # Auth Controller oluştur
        if secret_key:
            self.auth = AuthController(base_url, secret_key)
        else:
            self.auth = None
            
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Kullanıcı bilgilerini getirir
        
        Args:
            user_id (str): Kullanıcı ID'si
            
        Returns:
            Optional[Dict[str, Any]]: Kullanıcı bilgileri
        """
        try:
            self.logger.info(f"Kullanıcı bilgileri alınıyor: {user_id}")
            response = self.http.get(f"/users/{user_id}")
            return self.http.get_json(response)
        except Exception as e:
            self.logger.error(f"Kullanıcı bilgileri alınamadı: {str(e)}")
            return None
            
    def update_user_info(
        self,
        user_id: str,
        user_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Kullanıcı bilgilerini günceller
        
        Args:
            user_id (str): Kullanıcı ID'si
            user_data (Dict[str, Any]): Güncellenecek kullanıcı bilgileri
            
        Returns:
            Optional[Dict[str, Any]]: Güncellenmiş kullanıcı bilgileri
        """
        try:
            self.logger.info(f"Kullanıcı bilgileri güncelleniyor: {user_id}")
            response = self.http.put(
                f"/users/{user_id}",
                json=user_data
            )
            return self.http.get_json(response)
        except Exception as e:
            self.logger.error(f"Kullanıcı bilgileri güncellenemedi: {str(e)}")
            return None
            
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Yeni kullanıcı oluşturur
        
        Args:
            user_data (Dict[str, Any]): Kullanıcı bilgileri
            
        Returns:
            Optional[Dict[str, Any]]: Oluşturulan kullanıcı bilgileri
        """
        try:
            self.logger.info("Yeni kullanıcı oluşturuluyor")
            response = self.http.post("/users", json=user_data)
            return self.http.get_json(response)
        except Exception as e:
            self.logger.error(f"Kullanıcı oluşturulamadı: {str(e)}")
            return None
            
    def delete_user(self, user_id: str) -> bool:
        """
        Kullanıcıyı siler
        
        Args:
            user_id (str): Kullanıcı ID'si
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            self.logger.info(f"Kullanıcı siliniyor: {user_id}")
            response = self.http.delete(f"/users/{user_id}")
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Kullanıcı silinemedi: {str(e)}")
            return False
            
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Kullanıcı girişi yapar
        
        Args:
            username (str): Kullanıcı adı
            password (str): Şifre
            
        Returns:
            Optional[Dict[str, Any]]: Token ve kullanıcı bilgileri
        """
        if not self.auth:
            self.logger.error("Auth controller bulunamadı")
            return None
            
        try:
            self.logger.info(f"Kullanıcı girişi yapılıyor: {username}")
            return self.auth.login(username, password)
        except Exception as e:
            self.logger.error(f"Giriş başarısız: {str(e)}")
            return None
            
    def register(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Yeni kullanıcı kaydı oluşturur
        
        Args:
            user_data (Dict[str, Any]): Kullanıcı bilgileri
            
        Returns:
            Optional[Dict[str, Any]]: Token ve kullanıcı bilgileri
        """
        if not self.auth:
            self.logger.error("Auth controller bulunamadı")
            return None
            
        try:
            self.logger.info("Yeni kullanıcı kaydı oluşturuluyor")
            return self.auth.register(user_data)
        except Exception as e:
            self.logger.error(f"Kayıt başarısız: {str(e)}")
            return None
            
    def logout(self, token: str) -> bool:
        """
        Kullanıcı çıkışı yapar
        
        Args:
            token (str): JWT token
            
        Returns:
            bool: İşlem başarılı ise True
        """
        if not self.auth:
            self.logger.error("Auth controller bulunamadı")
            return False
            
        try:
            self.logger.info("Kullanıcı çıkışı yapılıyor")
            return self.auth.logout(token)
        except Exception as e:
            self.logger.error(f"Çıkış başarısız: {str(e)}")
            return False
            
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Token'ı doğrular
        
        Args:
            token (str): JWT token
            
        Returns:
            Optional[Dict[str, Any]]: Kullanıcı bilgileri
        """
        if not self.auth:
            self.logger.error("Auth controller bulunamadı")
            return None
            
        try:
            self.logger.info("Token doğrulanıyor")
            return self.auth.verify_token(token)
        except Exception as e:
            self.logger.error(f"Token doğrulanamadı: {str(e)}")
            return None
            
    def refresh_token(self, token: str) -> Optional[str]:
        """
        Token'ı yeniler
        
        Args:
            token (str): Eski JWT token
            
        Returns:
            Optional[str]: Yeni JWT token
        """
        if not self.auth:
            self.logger.error("Auth controller bulunamadı")
            return None
            
        try:
            self.logger.info("Token yenileniyor")
            return self.auth.refresh_token(token)
        except Exception as e:
            self.logger.error(f"Token yenilenemedi: {str(e)}")
            return None
