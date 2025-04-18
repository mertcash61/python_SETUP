import os
from typing import Dict, Any
from pathlib import Path

# Proje kök dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# Uygulama ayarları
APP_CONFIG = {
    'name': 'Setup Uygulaması',
    'version': '1.0.0',
    'debug': True,
    'timezone': 'Europe/Istanbul',
    'language': 'tr',
    'default_theme': 'light',
    'session_timeout': 3600,  # 1 saat
    'maintenance_mode': False,
    'admin_email': 'admin@example.com',
    'support_email': 'support@example.com'
}

# HTTP ayarları
HTTP_CONFIG = {
    'base_url': 'https://api.example.com',
    'timeout': 30,
    'max_retries': 3,
    'retry_delay': 1,
    'verify_ssl': True,
    'headers': {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Setup-App/1.0.0'
    },
    'proxy': {
        'enabled': False,
        'http': None,
        'https': None
    },
    'rate_limit': {
        'enabled': True,
        'requests': 100,
        'period': 60
    }
}

# Veritabanı ayarları
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'setup_db',
    'user': 'root',
    'password': '',  # Şifrenizi buraya girin
    'charset': 'utf32',
    'collation': 'utf32_turkish_ci',
    'use_unicode': True,
    'get_warnings': True,
    'raise_on_warnings': True,
    'connection_timeout': 10,
    'pool_name': 'mypool',
    'pool_size': 5,
    'backup': {
        'enabled': True,
        'interval': 'daily',
        'retention_days': 7,
        'path': 'backups'
    },
    'tables': {
        'users': """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(20),
                is_active BOOLEAN DEFAULT TRUE,
                is_admin BOOLEAN DEFAULT FALSE,
                last_login TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """,
        'sessions': """
            CREATE TABLE IF NOT EXISTS sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                token VARCHAR(255) NOT NULL,
                device_info TEXT,
                ip_address VARCHAR(45),
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """,
        'settings': """
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
        """,
        'logs': """
            CREATE TABLE IF NOT EXISTS logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                action VARCHAR(100) NOT NULL,
                description TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """,
        'notifications': """
            CREATE TABLE IF NOT EXISTS notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(50) NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """,
        'files': """
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL,
                original_name VARCHAR(255) NOT NULL,
                mime_type VARCHAR(100) NOT NULL,
                size INT NOT NULL,
                path VARCHAR(255) NOT NULL,
                is_public BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """,
        'api_keys': """
            CREATE TABLE IF NOT EXISTS api_keys (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                key VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                last_used TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """
    }
}

# Redis önbellek ayarları
CACHE_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
    'timeout': 300,  # 5 dakika
    'prefix': 'setup:',
    'compression': True,
    'key_expiration': {
        'session': 3600,  # 1 saat
        'token': 1800,    # 30 dakika
        'data': 86400     # 24 saat
    }
}

# JWT ayarları
JWT_CONFIG = {
    'secret_key': os.getenv('JWT_SECRET_KEY', 'your-secret-key'),
    'algorithm': 'HS256',
    'access_token_expire_minutes': 30,
    'refresh_token_expire_days': 7,
    'issuer': 'setup-app',
    'audience': ['web', 'mobile'],
    'blacklist_enabled': True
}

# Loglama ayarları
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/app.log',
    'max_size': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,
    'syslog': {
        'enabled': False,
        'host': 'localhost',
        'port': 514
    },
    'database': {
        'enabled': True,
        'table': 'logs'
    }
}

# Dosya yükleme ayarları
UPLOAD_CONFIG = {
    'allowed_extensions': ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'],
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'upload_dir': 'uploads',
    'temp_dir': 'temp',
    'virus_scan': True,
    'compression': {
        'enabled': True,
        'quality': 85
    },
    'storage': {
        'type': 'local',  # local, s3, azure
        'bucket': None,
        'region': None
    }
}

# Email ayarları
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'smtp_user': 'your-email@gmail.com',
    'smtp_password': os.getenv('EMAIL_PASSWORD', ''),
    'use_tls': True,
    'from_email': 'your-email@gmail.com',
    'from_name': 'Setup Uygulaması',
    'templates_dir': 'templates/email',
    'max_retries': 3,
    'retry_delay': 60,
    'queue': {
        'enabled': True,
        'max_attempts': 3
    }
}

# Güvenlik ayarları
SECURITY_CONFIG = {
    'allowed_hosts': ['localhost', '127.0.0.1'],
    'cors_origins': ['http://localhost:3000'],
    'rate_limit': {
        'enabled': True,
        'requests': 100,
        'period': 60  # 1 dakika
    },
    'password_policy': {
        'min_length': 8,
        'require_uppercase': True,
        'require_lowercase': True,
        'require_numbers': True,
        'require_special_chars': True,
        'max_age_days': 90,
        'history_size': 5
    },
    '2fa': {
        'enabled': True,
        'method': 'totp',  # totp veya sms
        'issuer': 'Setup App'
    },
    'session': {
        'timeout': 3600,
        'regenerate_id': True,
        'secure': True,
        'http_only': True
    }
}

# Sanal ortam ayarları
VENV_CONFIG = {
    'path': 'venv',
    'python_version': '3.8',
    'requirements_file': 'requirements.txt',
    'auto_activate': True,
    'backup': {
        'enabled': True,
        'interval': 'weekly',
        'retention_count': 4
    },
    'packages': {
        'auto_update': True,
        'check_interval': 86400  # 24 saat
    }
}

# API ayarları
API_CONFIG = {
    'version': 'v1',
    'prefix': '/api',
    'documentation': {
        'enabled': True,
        'path': '/docs',
        'title': 'Setup API',
        'description': 'Setup uygulaması API dokümantasyonu'
    },
    'rate_limit': {
        'enabled': True,
        'requests': 1000,
        'period': 3600  # 1 saat
    },
    'authentication': {
        'methods': ['jwt', 'api_key'],
        'default_method': 'jwt'
    }
}

# Bildirim ayarları
NOTIFICATION_CONFIG = {
    'email': {
        'enabled': True,
        'template_dir': 'templates/notifications'
    },
    'push': {
        'enabled': False,
        'provider': 'firebase',
        'credentials': None
    },
    'sms': {
        'enabled': False,
        'provider': 'twilio',
        'credentials': None
    },
    'queue': {
        'enabled': True,
        'max_attempts': 3
    }
}

def get_config(config_name: str) -> Dict[str, Any]:
    """
    Belirtilen yapılandırma ayarlarını döndürür
    
    Args:
        config_name (str): Yapılandırma adı
        
    Returns:
        Dict[str, Any]: Yapılandırma ayarları
    """
    configs = {
        'app': APP_CONFIG,
        'http': HTTP_CONFIG,
        'db': DB_CONFIG,
        'cache': CACHE_CONFIG,
        'jwt': JWT_CONFIG,
        'log': LOG_CONFIG,
        'upload': UPLOAD_CONFIG,
        'email': EMAIL_CONFIG,
        'security': SECURITY_CONFIG,
        'venv': VENV_CONFIG,
        'api': API_CONFIG,
        'notification': NOTIFICATION_CONFIG
    }
    return configs.get(config_name, {})

def update_config(config_name: str, new_config: Dict[str, Any]) -> bool:
    """
    Belirtilen yapılandırma ayarlarını günceller
    
    Args:
        config_name (str): Yapılandırma adı
        new_config (Dict[str, Any]): Yeni ayarlar
        
    Returns:
        bool: Güncelleme başarılı ise True
    """
    try:
        configs = {
            'app': APP_CONFIG,
            'http': HTTP_CONFIG,
            'db': DB_CONFIG,
            'cache': CACHE_CONFIG,
            'jwt': JWT_CONFIG,
            'log': LOG_CONFIG,
            'upload': UPLOAD_CONFIG,
            'email': EMAIL_CONFIG,
            'security': SECURITY_CONFIG,
            'venv': VENV_CONFIG,
            'api': API_CONFIG,
            'notification': NOTIFICATION_CONFIG
        }
        
        if config_name in configs:
            configs[config_name].update(new_config)
            return True
        return False
        
    except Exception as e:
        print(f"Yapılandırma güncellenirken hata oluştu: {str(e)}")
        return False

# Ortam değişkenlerinden yapılandırma yükleme
def load_env_config():
    """Ortam değişkenlerinden yapılandırma ayarlarını yükler"""
    try:
        # Veritabanı ayarları
        if os.getenv('DB_HOST'):
            DB_CONFIG['host'] = os.getenv('DB_HOST')
        if os.getenv('DB_PORT'):
            DB_CONFIG['port'] = int(os.getenv('DB_PORT'))
        if os.getenv('DB_NAME'):
            DB_CONFIG['database'] = os.getenv('DB_NAME')
        if os.getenv('DB_USER'):
            DB_CONFIG['user'] = os.getenv('DB_USER')
        if os.getenv('DB_PASSWORD'):
            DB_CONFIG['password'] = os.getenv('DB_PASSWORD')
            
        # JWT ayarları
        if os.getenv('JWT_SECRET_KEY'):
            JWT_CONFIG['secret_key'] = os.getenv('JWT_SECRET_KEY')
            
        # Email ayarları
        if os.getenv('SMTP_SERVER'):
            EMAIL_CONFIG['smtp_server'] = os.getenv('SMTP_SERVER')
        if os.getenv('SMTP_PORT'):
            EMAIL_CONFIG['smtp_port'] = int(os.getenv('SMTP_PORT'))
        if os.getenv('SMTP_USER'):
            EMAIL_CONFIG['smtp_user'] = os.getenv('SMTP_USER')
        if os.getenv('SMTP_PASSWORD'):
            EMAIL_CONFIG['smtp_password'] = os.getenv('SMTP_PASSWORD')
            
        # API ayarları
        if os.getenv('API_KEY'):
            API_CONFIG['key'] = os.getenv('API_KEY')
            
        # Bildirim ayarları
        if os.getenv('FIREBASE_CREDENTIALS'):
            NOTIFICATION_CONFIG['push']['credentials'] = os.getenv('FIREBASE_CREDENTIALS')
        if os.getenv('TWILIO_CREDENTIALS'):
            NOTIFICATION_CONFIG['sms']['credentials'] = os.getenv('TWILIO_CREDENTIALS')
            
    except Exception as e:
        print(f"Ortam değişkenleri yüklenirken hata oluştu: {str(e)}")

# Uygulama başlatıldığında ortam değişkenlerini yükle
load_env_config()

# Veritabanı tablolarını oluşturmak için SQL komutları
def create_database_tables():
    """
    Veritabanı tablolarını oluşturur
    
    Returns:
        str: SQL komutları
    """
    tables = DB_CONFIG['tables']
    sql_commands = []
    
    # Veritabanı oluştur
    sql_commands.append(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET {DB_CONFIG['charset']} COLLATE {DB_CONFIG['collation']};")
    sql_commands.append(f"USE {DB_CONFIG['database']};")
    
    # Tabloları oluştur
    for table_name, create_sql in tables.items():
        sql_commands.append(create_sql)
        
    return "\n".join(sql_commands)

# PhpMyAdmin için SQL komutlarını yazdır
if __name__ == "__main__":
    print("PhpMyAdmin için SQL komutları:")
    print(create_database_tables())
