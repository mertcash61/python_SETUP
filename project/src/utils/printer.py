class Printer:
    """
    Kullanıcıya bilgi yazdırmak için yardımcı sınıf.
    """
    
    @staticmethod
    def print_info(message: str) -> None:
        """
        Bilgi mesajını yazdırır
        
        Args:
            message (str): Yazdırılacak mesaj
        """
        print(f"INFO: {message}")

    @staticmethod
    def print_error(message: str) -> None:
        """
        Hata mesajını yazdırır
        
        Args:
            message (str): Yazdırılacak mesaj
        """
        print(f"ERROR: {message}")

    @staticmethod
    def print_warning(message: str) -> None:
        """
        Uyarı mesajını yazdırır
        
        Args:
            message (str): Yazdırılacak mesaj
        """
        print(f"WARNING: {message}")
