import os
import sys
import subprocess
import logging
import getpass
import platform
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import hashlib
import secrets
from datetime import datetime

class SetupScript:
    """
    Setup uygulaması için kurulum scriptleri.
    
    Bu sınıf, veritabanı kurulumu, sanal ortam oluşturma ve yapılandırma
    dosyalarını oluşturma işlemlerini yönetir.
    """
    
    def __init__(self):
        """SetupScript sınıfı başlatıcısı"""
        # Loglama ayarları
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Konsol log handler'ı
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Dosya log handler'ı
        log_file = Path(__file__).parent.parent / "logs" / "setup.log"
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Proje dizinleri
        self.project_root = Path(__file__).parent.parent
        self.database_dir = self.project_root / "database"
        self.config_dir = self.project_root / "config"
        self.venv_dir = self.project_root / "venv"
        self.backup_dir = self.project_root / "backups"
        
        # Sistem bilgileri
        self.system_info = {
            'os': platform.system(),
            'python_version': platform.python_version(),
            'architecture': platform.machine()
        }
        
    def check_prerequisites(self) -> bool:
        """
        Kurulum öncesi gerekli kontrolleri yapar
        
        Returns:
            bool: Tüm kontroller başarılı ise True
        """
        try:
            self.logger.info("Ön kontroller başlatılıyor...")
            
            # Python versiyon kontrolü
            if sys.version_info < (3, 8):
                self.logger.error("Python 3.8 veya üstü gerekli")
                return False
                
            # MySQL kontrolü
            try:
                subprocess.run(['mysql', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.logger.error("MySQL yüklü değil")
                return False
                
            # Dizin yazma izinleri kontrolü
            for directory in [self.database_dir, self.config_dir, self.venv_dir, self.backup_dir]:
                if not os.access(directory.parent, os.W_OK):
                    self.logger.error(f"{directory} dizinine yazma izni yok")
                    return False
                    
            self.logger.info("Ön kontroller başarılı")
            return True
            
        except Exception as e:
            self.logger.error(f"Ön kontroller sırasında hata: {str(e)}")
            return False
            
    def backup_existing_config(self) -> bool:
        """
        Mevcut yapılandırma dosyalarını yedekler
        
        Returns:
            bool: Yedekleme başarılı ise True
        """
        try:
            self.logger.info("Mevcut yapılandırmalar yedekleniyor...")
            
            # Yedek dizini oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"config_backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Config dosyalarını yedekle
            if self.config_dir.exists():
                for config_file in self.config_dir.glob("*.py"):
                    shutil.copy2(config_file, backup_path / config_file.name)
                    
            self.logger.info("Yedekleme tamamlandı")
            return True
            
        except Exception as e:
            self.logger.error(f"Yedekleme sırasında hata: {str(e)}")
            return False
            
    def generate_secret_key(self) -> str:
        """
        Güvenli bir secret key oluşturur
        
        Returns:
            str: Oluşturulan secret key
        """
        return secrets.token_urlsafe(32)
        
    def setup_database(self) -> bool:
        """
        Veritabanı kurulumunu gerçekleştirir
        
        Returns:
            bool: Kurulum başarılı ise True
        """
        try:
            self.logger.info("Veritabanı kurulumu başlatılıyor...")
            
            # MySQL kullanıcı bilgilerini al
            db_user = input("MySQL kullanıcı adı [root]: ") or "root"
            db_password = getpass.getpass("MySQL şifresi: ")
            
            # SQL dosyasının yolu
            sql_file = self.database_dir / "setup_db.sql"
            
            if not sql_file.exists():
                self.logger.error("SQL dosyası bulunamadı")
                return False
                
            # MySQL komutunu çalıştır
            cmd = f"mysql -u {db_user} -p{db_password} < {sql_file}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("Veritabanı kurulumu başarılı")
                return True
            else:
                self.logger.error(f"Veritabanı kurulumu başarısız: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Veritabanı kurulumu sırasında hata: {str(e)}")
            return False
            
    def setup_venv(self) -> bool:
        """
        Sanal ortam kurulumunu gerçekleştirir
        
        Returns:
            bool: Kurulum başarılı ise True
        """
        try:
            self.logger.info("Sanal ortam kurulumu başlatılıyor...")
            
            # Eski sanal ortamı temizle
            if self.venv_dir.exists():
                shutil.rmtree(self.venv_dir)
                
            # Sanal ortam oluştur
            cmd = f"python -m venv {self.venv_dir}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"Sanal ortam oluşturulamadı: {result.stderr}")
                return False
                
            # Gerekli paketleri yükle
            requirements_file = self.project_root / "requirements.txt"
            if requirements_file.exists():
                # Windows için
                if self.system_info['os'] == "Windows":
                    activate_cmd = f"{self.venv_dir}/Scripts/activate && pip install -r {requirements_file}"
                # Linux/Mac için
                else:
                    activate_cmd = f"source {self.venv_dir}/bin/activate && pip install -r {requirements_file}"
                    
                result = subprocess.run(activate_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    self.logger.error(f"Paketler yüklenemedi: {result.stderr}")
                    return False
                    
            self.logger.info("Sanal ortam kurulumu başarılı")
            return True
            
        except Exception as e:
            self.logger.error(f"Sanal ortam kurulumu sırasında hata: {str(e)}")
            return False
            
    def setup_config(self) -> bool:
        """
        Yapılandırma dosyalarını oluşturur
        
        Returns:
            bool: Kurulum başarılı ise True
        """
        try:
            self.logger.info("Yapılandırma dosyaları oluşturuluyor...")
            
            # Config dizini oluştur
            self.config_dir.mkdir(exist_ok=True)
            
            # Güvenli secret key oluştur
            secret_key = self.generate_secret_key()
            
            # settings.py dosyasını oluştur
            settings_file = self.config_dir / "settings.py"
            if not settings_file.exists():
                with open(settings_file, "w", encoding="utf-8") as f:
                    f.write(f"""# Uygulama ayarları
APP_CONFIG = {{
    'name': 'Setup Uygulaması',
    'version': '1.0.0',
    'debug': True,
    'timezone': 'Europe/Istanbul',
    'language': 'tr',
    'default_theme': 'light',
    'secret_key': '{secret_key}'
}}

# Veritabanı ayarları
DB_CONFIG = {{
    'host': 'localhost',
    'port': 3306,
    'database': 'setup_db',
    'user': 'root',
    'password': '',
    'charset': 'utf32',
    'collation': 'utf32_turkish_ci'
}}

# HTTP ayarları
HTTP_CONFIG = {{
    'base_url': 'http://localhost:8000',
    'timeout': 30,
    'max_retries': 3,
    'ssl_verify': True
}}

# JWT ayarları
JWT_CONFIG = {{
    'secret_key': '{secret_key}',
    'algorithm': 'HS256',
    'access_token_expire_minutes': 30,
    'refresh_token_expire_days': 7
}}

# Güvenlik ayarları
SECURITY_CONFIG = {{
    'password_min_length': 8,
    'password_require_uppercase': True,
    'password_require_lowercase': True,
    'password_require_numbers': True,
    'password_require_special': True,
    'session_timeout': 3600,
    'max_login_attempts': 5
}}

# Loglama ayarları
LOG_CONFIG = {{
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/app.log',
    'max_size': 10 * 1024 * 1024,
    'backup_count': 5
}}
""")
                    
            self.logger.info("Yapılandırma dosyaları oluşturuldu")
            return True
            
        except Exception as e:
            self.logger.error(f"Yapılandırma dosyaları oluşturulurken hata: {str(e)}")
            return False
            
    def run_setup(self) -> bool:
        """
        Tüm kurulum adımlarını sırasıyla çalıştırır
        
        Returns:
            bool: Tüm kurulumlar başarılı ise True
        """
        try:
            self.logger.info("Kurulum başlatılıyor...")
            
            # Ön kontroller
            if not self.check_prerequisites():
                return False
                
            # Mevcut yapılandırmaları yedekle
            if not self.backup_existing_config():
                return False
                
            # Veritabanı kurulumu
            if not self.setup_database():
                return False
                
            # Sanal ortam kurulumu
            if not self.setup_venv():
                return False
                
            # Yapılandırma dosyaları
            if not self.setup_config():
                return False
                
            self.logger.info("Kurulum başarıyla tamamlandı")
            return True
            
        except Exception as e:
            self.logger.error(f"Kurulum sırasında hata: {str(e)}")
            return False

def main():
    """Ana fonksiyon"""
    setup = SetupScript()
    if setup.run_setup():
        print("Kurulum başarıyla tamamlandı!")
    else:
        print("Kurulum sırasında hata oluştu!")
        sys.exit(1)

if __name__ == "__main__":
    main()
