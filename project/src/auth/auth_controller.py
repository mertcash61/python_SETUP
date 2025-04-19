import jwt
import datetime
from typing import Dict, Any, Optional
import logging
import bcrypt

class AuthController:
    """
    Kullanıcı kimlik doğrulama işlemlerini yöneten sınıf.
    """
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        """
        AuthController sınıfı başlatıcısı
        
        Args:
            secret_key (str): JWT için gizli anahtar
            algorithm (str): JWT algoritması
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.users = {}  # Basit bir kullanıcı veritabanı
        
        # Loglama ayarları
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def register_user(self, username: str, password: str) -> None:
        """
        Yeni kullanıcı kaydı yapar
        
        Args:
            username (str): Kullanıcı adı
            password (str): Şifre
        """
        if username in self.users:
            self.logger.error("Kullanıcı zaten kayıtlı")
            raise ValueError("Kullanıcı zaten kayıtlı")
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = hashed_password
        self.logger.info(f"Kullanıcı kaydedildi: {username}")

    def login_user(self, username: str, password: str) -> str:
        """
        Kullanıcı girişi yapar ve JWT döndürür
        
        Args:
            username (str): Kullanıcı adı
            password (str): Şifre
            
        Returns:
            str: JWT
        """
        if username not in self.users:
            self.logger.error("Kullanıcı bulunamadı")
            raise ValueError("Kullanıcı bulunamadı")
        
        if not bcrypt.checkpw(password.encode('utf-8'), self.users[username]):
            self.logger.error("Şifre yanlış")
            raise ValueError("Şifre yanlış")
        
        return self.generate_token(username)

    def verify_password(self, username: str, password: str) -> bool:
        """
        Kullanıcı şifresini doğrular
        
        Args:
            username (str): Kullanıcı adı
            password (str): Şifre
            
        Returns:
            bool: Doğrulama başarılı ise True
        """
        if username not in self.users:
            self.logger.error("Kullanıcı bulunamadı")
            return False
        
        if bcrypt.checkpw(password.encode('utf-8'), self.users[username]):
            self.logger.info("Şifre doğrulandı")
            return True
        else:
            self.logger.error("Şifre yanlış")
            return False

    def generate_token(self, user_id: str, expires_in: int = 3600) -> str:
        """
        Kullanıcı için JWT oluşturur
        
        Args:
            user_id (str): Kullanıcı ID'si
            expires_in (int): Token geçerlilik süresi (saniye)
            
        Returns:
            str: JWT
        """
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
            }
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            self.logger.info(f"Token oluşturuldu: {token}")
            return token
        except Exception as e:
            self.logger.error(f"Token oluşturma hatası: {str(e)}")
            raise

    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        JWT doğrular ve yükü döndürür
        
        Args:
            token (str): Doğrulanacak JWT
            
        Returns:
            Dict[str, Any]: Token yükü
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            self.logger.info(f"Token doğrulandı: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.error("Token süresi dolmuş")
            raise
        except jwt.InvalidTokenError:
            self.logger.error("Geçersiz token")
            raise

    def update_user(self, username: str, new_password: Optional[str] = None) -> None:
        """
        Kullanıcı bilgilerini günceller
        
        Args:
            username (str): Kullanıcı adı
            new_password (Optional[str]): Yeni şifre
        """
        if username not in self.users:
            self.logger.error("Kullanıcı bulunamadı")
            raise ValueError("Kullanıcı bulunamadı")
        
        if new_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self.users[username] = hashed_password
            self.logger.info(f"Kullanıcı şifresi güncellendi: {username}")

    def delete_user(self, username: str) -> None:
        """
        Kullanıcıyı sistemden siler
        
        Args:
            username (str): Kullanıcı adı
        """
        if username in self.users:
            del self.users[username]
            self.logger.info(f"Kullanıcı silindi: {username}")
        else:
            self.logger.error("Kullanıcı bulunamadı")
            raise ValueError("Kullanıcı bulunamadı")
