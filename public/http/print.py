from typing import Dict, Any, Optional
import json
from datetime import datetime

def print_response(
    response_data: Dict[str, Any],
    pretty: bool = True,
    show_timestamp: bool = True
) -> None:
    """
    HTTP yanıtını yazdırır
    
    Args:
        response_data (Dict[str, Any]): Yanıt verisi
        pretty (bool): JSON'ı güzel formatla yazdır
        show_timestamp (bool): Zaman damgası göster
    """
    if show_timestamp:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
    if pretty:
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(response_data, ensure_ascii=False))

def print_error(
    error_message: str,
    error_details: Optional[Dict[str, Any]] = None,
    show_timestamp: bool = True
) -> None:
    """
    Hata mesajını yazdırır
    
    Args:
        error_message (str): Hata mesajı
        error_details (Dict[str, Any], optional): Hata detayları
        show_timestamp (bool): Zaman damgası göster
    """
    if show_timestamp:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
    print(f"❌ Hata: {error_message}")
    if error_details:
        print("Hata Detayları:")
        print(json.dumps(error_details, indent=2, ensure_ascii=False))

def print_success(
    message: str,
    data: Optional[Dict[str, Any]] = None,
    show_timestamp: bool = True
) -> None:
    """
    Başarı mesajını yazdırır
    
    Args:
        message (str): Başarı mesajı
        data (Dict[str, Any], optional): Ek veri
        show_timestamp (bool): Zaman damgası göster
    """
    if show_timestamp:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
    print(f"✅ {message}")
    if data:
        print("Veri:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

def print_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    show_timestamp: bool = True
) -> None:
    """
    HTTP isteğini yazdırır
    
    Args:
        method (str): HTTP metodu
        url (str): İstek URL'i
        headers (Dict[str, str], optional): İstek başlıkları
        data (Dict[str, Any], optional): İstek verisi
        show_timestamp (bool): Zaman damgası göster
    """
    if show_timestamp:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
    print(f"🌐 {method} {url}")
    
    if headers:
        print("Başlıklar:")
        for key, value in headers.items():
            if key.lower() in ["authorization", "x-api-key"]:
                value = "***"  # Hassas bilgileri gizle
            print(f"  {key}: {value}")
            
    if data:
        print("Veri:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

def print_user_info(
    user_data: Dict[str, Any],
    show_timestamp: bool = True
) -> None:
    """
    Kullanıcı bilgilerini yazdırır
    
    Args:
        user_data (Dict[str, Any]): Kullanıcı bilgileri
        show_timestamp (bool): Zaman damgası göster
    """
    if show_timestamp:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
    print("👤 Kullanıcı Bilgileri:")
    for key, value in user_data.items():
        if key.lower() in ["password", "token"]:
            value = "***"  # Hassas bilgileri gizle
        print(f"  {key}: {value}")
