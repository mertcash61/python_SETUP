import os
import sys
import subprocess
from typing import Optional, List, Dict
from pathlib import Path

class VirtualEnvironment:
    """
    Python sanal ortam yönetimi için temel sınıf.
    
    Bu sınıf, sanal ortam oluşturma, paket yönetimi ve ortam değişkenleri
    yönetimi için gerekli metodları içerir.
    """
    
    def __init__(self, venv_path: str):
        """
        Sanal ortam sınıfı başlatıcısı
        
        Args:
            venv_path (str): Sanal ortam dizini yolu
        """
        self.venv_path = Path(venv_path).absolute()
        self.python_path = self.venv_path / "Scripts" / "python.exe"
        self.pip_path = self.venv_path / "Scripts" / "pip.exe"
        
    def create(self, python_path: Optional[str] = None) -> bool:
        """
        Yeni bir sanal ortam oluşturur
        
        Args:
            python_path (str, optional): Python yorumlayıcı yolu
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            cmd = [sys.executable, "-m", "venv", str(self.venv_path)]
            if python_path:
                cmd.extend(["--python", python_path])
                
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def install_packages(self, packages: List[str]) -> bool:
        """
        Paketleri sanal ortama yükler
        
        Args:
            packages (List[str]): Yüklenecek paket listesi
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            cmd = [str(self.pip_path), "install"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def uninstall_packages(self, packages: List[str]) -> bool:
        """
        Paketleri sanal ortamdan kaldırır
        
        Args:
            packages (List[str]): Kaldırılacak paket listesi
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            cmd = [str(self.pip_path), "uninstall", "-y"] + packages
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def get_installed_packages(self) -> Dict[str, str]:
        """
        Yüklü paketleri listeler
        
        Returns:
            Dict[str, str]: Paket adı ve versiyon bilgileri
        """
        try:
            result = subprocess.run(
                [str(self.pip_path), "freeze"],
                capture_output=True,
                text=True,
                check=True
            )
            packages = {}
            for line in result.stdout.splitlines():
                if "==" in line:
                    name, version = line.split("==")
                    packages[name] = version
            return packages
        except subprocess.CalledProcessError:
            return {}
            
    def activate(self) -> bool:
        """
        Sanal ortamı aktifleştirir
        
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            activate_script = self.venv_path / "Scripts" / "activate.bat"
            subprocess.run([str(activate_script)], shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def deactivate(self) -> bool:
        """
        Sanal ortamı deaktif eder
        
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            subprocess.run(["deactivate"], shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def exists(self) -> bool:
        """
        Sanal ortamın var olup olmadığını kontrol eder
        
        Returns:
            bool: Sanal ortam varsa True
        """
        return self.venv_path.exists() and self.python_path.exists()
