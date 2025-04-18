import mysql.connector
from mysql.connector import Error
import logging

class DatabaseSetup:
    def __init__(self, host, user, password, database):
        """
        Veritabanı bağlantısı için gerekli bilgileri alır
        
        Args:
            host (str): Veritabanı sunucusu
            user (str): Veritabanı kullanıcı adı
            password (str): Veritabanı şifresi
            database (str): Veritabanı adı
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # Loglama ayarları
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def connect(self):
        """Veritabanına bağlantı kurar"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.logger.info(f"MySQL veritabanına başarıyla bağlanıldı: {self.database}")
                self.cursor = self.connection.cursor()
                return True
        except Error as e:
            self.logger.error(f"MySQL bağlantı hatası: {str(e)}")
            return False
            
    def create_tables(self):
        """Gerekli tabloları oluşturur"""
        try:
            # Kullanıcılar tablosu
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            # Oturumlar tablosu
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Ayarlar tablosu
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    setting_key VARCHAR(50) NOT NULL,
                    setting_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_setting (user_id, setting_key)
                )
            """)
            
            # Loglar tablosu
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(100) NOT NULL,
                    description TEXT,
                    ip_address VARCHAR(45),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                )
            """)
            
            self.connection.commit()
            self.logger.info("Tablolar başarıyla oluşturuldu")
            return True
            
        except Error as e:
            self.logger.error(f"Tablo oluşturma hatası: {str(e)}")
            return False
            
    def close(self):
        """Veritabanı bağlantısını kapatır"""
        try:
            if hasattr(self, 'cursor'):
                self.cursor.close()
            if hasattr(self, 'connection') and self.connection.is_connected():
                self.connection.close()
                self.logger.info("MySQL bağlantısı kapatıldı")
        except Error as e:
            self.logger.error(f"Bağlantı kapatma hatası: {str(e)}")

if __name__ == "__main__":
    # Veritabanı bağlantı bilgileri
    DB_CONFIG = {
        'host': 'localhost',  # Veritabanı sunucunuzun adresi
        'user': 'root',      # MySQL kullanıcı adınız
        'password': '',      # MySQL şifreniz
        'database': 'setup_db'  # Oluşturduğunuz veritabanının adı
    }
    
    # Veritabanı kurulumu
    db_setup = DatabaseSetup(**DB_CONFIG)
    
    if db_setup.connect():
        if db_setup.create_tables():
            print("Veritabanı kurulumu başarıyla tamamlandı!")
        else:
            print("Tablo oluşturma sırasında hata oluştu!")
    else:
        print("Veritabanına bağlanılamadı!")
        
    db_setup.close()
