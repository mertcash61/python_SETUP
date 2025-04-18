from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
import mysql.connector
import hashlib
import logging
from pathlib import Path

class AuthController:
    """
    Setup uygulaması için kimlik doğrulama controller sınıfı.
    
    Bu sınıf, kullanıcı yönetimi, oturum kontrolü ve güvenlik 
    işlemlerini yönetir.
    """
    
    def __init__(
        self,
        db_config: Dict[str, Any],
        secret_key: str,
        token_expire_minutes: int = 30
    ):
        """
        Auth Controller sınıfı başlatıcısı
        
        Args:
            db_config (Dict[str, Any]): Veritabanı bağlantı ayarları
            secret_key (str): JWT token imzalama anahtarı
            token_expire_minutes (int): Token geçerlilik süresi (dakika)
        """
        self.db_config = db_config
        self.secret_key = secret_key
        self.token_expire_minutes = token_expire_minutes
        
        # Loglama ayarları
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "auth.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _get_db_connection(self):
        """Veritabanı bağlantısı oluşturur"""
        try:
            return mysql.connector.connect(**self.db_config)
        except Exception as e:
            self.logger.error(f"Veritabanı bağlantı hatası: {e}")
            raise
            
    def _hash_password(self, password: str) -> str:
        """Şifreyi güvenli bir şekilde hashler"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Kullanıcı girişi yapar ve token oluşturur
        
        Args:
            username (str): Kullanıcı adı
            password (str): Şifre
            
        Returns:
            Optional[Dict[str, Any]]: Token ve kullanıcı bilgileri
        """
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Kullanıcıyı kontrol et
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, self._hash_password(password))
            )
            user = cursor.fetchone()
            
            if user:
                # Hassas bilgileri temizle
                user.pop('password', None)
                
                # Son giriş zamanını güncelle
                cursor.execute(
                    "UPDATE users SET last_login = NOW() WHERE id = %s",
                    (user['id'],)
                )
                conn.commit()
                
                # Oturum kaydı oluştur
                cursor.execute(
                    """
                    INSERT INTO sessions (user_id, token, device_info, ip_address)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user['id'], self._create_token(user), 'Setup App', '127.0.0.1')
                )
                conn.commit()
                
                self.logger.info(f"Kullanıcı girişi başarılı: {username}")
                return {
                    "token": self._create_token(user),
                    "user": user
                }
                
            self.logger.warning(f"Geçersiz giriş denemesi: {username}")
            return None
            
        except Exception as e:
            self.logger.error(f"Giriş hatası: {e}")
            return None
            
        finally:
            cursor.close()
            conn.close()
            
    def register(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Yeni kullanıcı kaydı oluşturur
        
        Args:
            user_data (Dict[str, Any]): Kullanıcı bilgileri
            
        Returns:
            Optional[Dict[str, Any]]: Oluşturulan kullanıcı bilgileri
        """
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Kullanıcı adı ve email kontrolü
            cursor.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (user_data['username'], user_data['email'])
            )
            if cursor.fetchone():
                self.logger.warning(f"Kullanıcı zaten mevcut: {user_data['username']}")
                return None
                
            # Yeni kullanıcı oluştur
            sql = """
                INSERT INTO users (
                    username, email, password, first_name, last_name,
                    is_active, is_admin
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                user_data['username'],
                user_data['email'],
                self._hash_password(user_data['password']),
                user_data.get('first_name', ''),
                user_data.get('last_name', ''),
                True,
                False
            )
            
            cursor.execute(sql, values)
            conn.commit()
            
            # Oluşturulan kullanıcıyı getir
            cursor.execute(
                "SELECT * FROM users WHERE id = %s",
                (cursor.lastrowid,)
            )
            user = cursor.fetchone()
            user.pop('password', None)
            
            self.logger.info(f"Yeni kullanıcı kaydı oluşturuldu: {user_data['username']}")
            return {
                "token": self._create_token(user),
                "user": user
            }
            
        except Exception as e:
            self.logger.error(f"Kayıt hatası: {e}")
            return None
            
        finally:
            cursor.close()
            conn.close()
            
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Token'ı doğrular ve kullanıcı bilgilerini döndürür
        
        Args:
            token (str): JWT token
            
        Returns:
            Optional[Dict[str, Any]]: Kullanıcı bilgileri
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            
            # Token'ın geçerliliğini veritabanından kontrol et
            conn = self._get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                SELECT s.*, u.* FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.token = %s AND s.expires_at > NOW()
                """,
                (token,)
            )
            session = cursor.fetchone()
            
            if session:
                session.pop('password', None)
                return session
                
            return None
            
        except jwt.InvalidTokenError:
            self.logger.warning(f"Geçersiz token: {token}")
            return None
            
        except Exception as e:
            self.logger.error(f"Token doğrulama hatası: {e}")
            return None
            
        finally:
            cursor.close()
            conn.close()
            
    def logout(self, token: str) -> bool:
        """
        Kullanıcı çıkışı yapar
        
        Args:
            token (str): JWT token
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Oturumu sonlandır
            cursor.execute(
                "DELETE FROM sessions WHERE token = %s",
                (token,)
            )
            conn.commit()
            
            self.logger.info("Kullanıcı çıkışı yapıldı")
            return True
            
        except Exception as e:
            self.logger.error(f"Çıkış hatası: {e}")
            return False
            
        finally:
            cursor.close()
            conn.close()
            
    def _create_token(self, user_data: Dict[str, Any]) -> str:
        """
        JWT token oluşturur
        
        Args:
            user_data (Dict[str, Any]): Kullanıcı bilgileri
            
        Returns:
            str: JWT token
        """
        expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
        payload = {
            "user": user_data,
            "exp": expire
        }
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm="HS256"
        )
        
        # Token'ı veritabanına kaydet
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                UPDATE sessions 
                SET expires_at = %s
                WHERE token = %s
                """,
                (expire, token)
            )
            conn.commit()
            
        except Exception as e:
            self.logger.error(f"Token kayıt hatası: {e}")
            
        finally:
            cursor.close()
            conn.close()
            
        return token
