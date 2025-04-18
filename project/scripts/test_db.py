import mysql.connector
from mysql.connector import Error
import logging
from pathlib import Path

def test_database_connection():
    """
    Veritabanı bağlantısını test eder
    """
    # Loglama ayarları
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/db_test.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Veritabanı bağlantı bilgileri
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': input("MySQL şifrenizi girin: "),
            'database': 'setup_db'
        }
        
        logger.info("Veritabanına bağlanılıyor...")
        
        # Bağlantıyı oluştur
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            logger.info(f"MySQL sunucusuna bağlandı: {db_info}")
            
            # Veritabanı adını al
            cursor = connection.cursor()
            cursor.execute("select database();")
            database = cursor.fetchone()
            logger.info(f"Veritabanı: {database[0]}")
            
            # Tabloları listele
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            logger.info("Mevcut tablolar:")
            for table in tables:
                logger.info(f"- {table[0]}")
                
            # Bağlantıyı kapat
            cursor.close()
            connection.close()
            logger.info("Veritabanı bağlantısı kapatıldı")
            
    except Error as e:
        logger.error(f"Veritabanı bağlantı hatası: {e}")
        
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")

if __name__ == "__main__":
    test_database_connection() 