import numpy as np
import pandas as pd
import requests

def create_sample_data(func='sin'):
    """Örnek veri oluşturma."""
    x = np.linspace(0, 10, 50)
    if func == 'sin':
        y = np.sin(x)
    elif func == 'cos':
        y = np.cos(x)
    else:
        raise ValueError("Geçersiz fonksiyon. 'sin' veya 'cos' kullanın.")
    
    return pd.DataFrame({'x': x, 'y': y})

def fetch_data(url):
    """HTTP isteği yapma."""
    response = requests.get(url)
    if response.status_code == 200:
        print("Veri başarıyla alındı.")
        return response.json()  # JSON formatında veri döndür
    else:
        print("Veri alınırken bir hata oluştu.")
        return None
