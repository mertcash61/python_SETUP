from datetime import datetime
from typing import Dict

class UserSessionManager:
    """
    Kullanıcı giriş ve çıkışlarını kontrol eden yönetici sınıfı.
    """
    
    def __init__(self):
        """
        UserSessionManager sınıfı başlatıcısı
        """
        self.active_sessions: Dict[str, datetime] = {}

    def login(self, username: str) -> None:
        """
        Kullanıcıyı sisteme giriş yapmış olarak kaydeder
        
        Args:
            username (str): Kullanıcı adı
        """
        self.active_sessions[username] = datetime.now()
        print(f"{username} giriş yaptı.")

    def logout(self, username: str) -> None:
        """
        Kullanıcıyı sistemden çıkış yapmış olarak kaydeder
        
        Args:
            username (str): Kullanıcı adı
        """
        if username in self.active_sessions:
            del self.active_sessions[username]
            print(f"{username} çıkış yaptı.")
        else:
            print(f"{username} zaten çıkış yapmış.")

    def is_logged_in(self, username: str) -> bool:
        """
        Kullanıcının sisteme giriş yapıp yapmadığını kontrol eder
        
        Args:
            username (str): Kullanıcı adı
            
        Returns:
            bool: Kullanıcı giriş yapmışsa True, aksi halde False
        """
        return username in self.active_sessions 

    def get_session_duration(self, username: str) -> str:
        """
        Kullanıcının oturum süresini döndürür
        
        Args:
            username (str): Kullanıcı adı
            
        Returns:
            str: Oturum süresi (saat:dakika:saniye)
        """
        if username in self.active_sessions:
            session_start = self.active_sessions[username]
            duration = datetime.now() - session_start
            return str(duration)
        else:
            return "Kullanıcı giriş yapmamış."

    def list_active_sessions(self) -> None:
        """
        Aktif oturumları listeler
        """
        if self.active_sessions:
            print("Aktif oturumlar:")
            for username, start_time in self.active_sessions.items():
                print(f"{username} - Başlangıç: {start_time}")
        else:
            print("Aktif oturum yok.") 