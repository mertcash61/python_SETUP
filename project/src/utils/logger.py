import logging

class Logger:
    """
    Uygulama genelinde loglama işlemlerini yöneten sınıf.
    """
    
    def __init__(self, name: str):
        """
        Logger sınıfı başlatıcısı
        
        Args:
            name (str): Logger adı
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Konsol için handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Log formatı
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Handler'ı logger'a ekle
        self.logger.addHandler(console_handler)

    def info(self, message: str) -> None:
        """
        Bilgi seviyesinde loglama yapar
        
        Args:
            message (str): Log mesajı
        """
        self.logger.info(message)

    def error(self, message: str) -> None:
        """
        Hata seviyesinde loglama yapar
        
        Args:
            message (str): Log mesajı
        """
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """
        Uyarı seviyesinde loglama yapar
        
        Args:
            message (str): Log mesajı
        """
        self.logger.warning(message)
