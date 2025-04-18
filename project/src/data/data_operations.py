import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import json

class DataOperations:
    """
    Veri işleme operasyonları için temel sınıf.
    
    Bu sınıf, veri temizleme, dönüştürme ve hazırlama işlemlerini yönetir.
    """
    
    def __init__(self):
        """DataOperations sınıfı başlatıcısı"""
        # Loglama ayarları
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "data_operations.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_data(self, file_path: str, file_type: str = 'csv') -> Optional[pd.DataFrame]:
        """
        Veri dosyasını yükler
        
        Args:
            file_path (str): Dosya yolu
            file_type (str): Dosya tipi (csv, excel, json)
            
        Returns:
            Optional[pd.DataFrame]: Yüklenen veri
        """
        try:
            if file_type == 'csv':
                data = pd.read_csv(file_path)
            elif file_type == 'excel':
                data = pd.read_excel(file_path)
            elif file_type == 'json':
                data = pd.read_json(file_path)
            else:
                raise ValueError(f"Desteklenmeyen dosya tipi: {file_type}")
                
            self.logger.info(f"Veri başarıyla yüklendi: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Veri yükleme hatası: {e}")
            return None
            
    def clean_data(self, data: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """
        Veriyi temizler
        
        Args:
            data (pd.DataFrame): Temizlenecek veri
            config (Dict[str, Any]): Temizleme ayarları
            
        Returns:
            pd.DataFrame: Temizlenmiş veri
        """
        try:
            # Eksik değerleri işle
            if 'missing_values' in config:
                strategy = config['missing_values'].get('strategy', 'mean')
                if strategy == 'mean':
                    data = data.fillna(data.mean())
                elif strategy == 'median':
                    data = data.fillna(data.median())
                elif strategy == 'mode':
                    data = data.fillna(data.mode().iloc[0])
                elif strategy == 'drop':
                    data = data.dropna()
                    
            # Aykırı değerleri işle
            if 'outliers' in config:
                method = config['outliers'].get('method', 'zscore')
                threshold = config['outliers'].get('threshold', 3)
                
                if method == 'zscore':
                    z_scores = np.abs((data - data.mean()) / data.std())
                    data = data[(z_scores < threshold).all(axis=1)]
                elif method == 'iqr':
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    data = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]
                    
            # Kategorik değişkenleri dönüştür
            if 'categorical' in config:
                method = config['categorical'].get('method', 'onehot')
                columns = config['categorical'].get('columns', [])
                
                if method == 'onehot':
                    data = pd.get_dummies(data, columns=columns)
                elif method == 'label':
                    for col in columns:
                        data[col] = data[col].astype('category').cat.codes
                        
            self.logger.info("Veri başarıyla temizlendi")
            return data
            
        except Exception as e:
            self.logger.error(f"Veri temizleme hatası: {e}")
            return data
            
    def normalize_data(self, data: pd.DataFrame, method: str = 'minmax') -> pd.DataFrame:
        """
        Veriyi normalize eder
        
        Args:
            data (pd.DataFrame): Normalize edilecek veri
            method (str): Normalizasyon metodu (minmax, standard)
            
        Returns:
            pd.DataFrame: Normalize edilmiş veri
        """
        try:
            if method == 'minmax':
                return (data - data.min()) / (data.max() - data.min())
            elif method == 'standard':
                return (data - data.mean()) / data.std()
            else:
                raise ValueError(f"Desteklenmeyen normalizasyon metodu: {method}")
                
        except Exception as e:
            self.logger.error(f"Veri normalizasyon hatası: {e}")
            return data
            
    def save_data(self, data: pd.DataFrame, file_path: str, file_type: str = 'csv') -> bool:
        """
        Veriyi kaydeder
        
        Args:
            data (pd.DataFrame): Kaydedilecek veri
            file_path (str): Kayıt yolu
            file_type (str): Dosya tipi (csv, excel, json)
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            if file_type == 'csv':
                data.to_csv(file_path, index=False)
            elif file_type == 'excel':
                data.to_excel(file_path, index=False)
            elif file_type == 'json':
                data.to_json(file_path, orient='records')
            else:
                raise ValueError(f"Desteklenmeyen dosya tipi: {file_type}")
                
            self.logger.info(f"Veri başarıyla kaydedildi: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Veri kaydetme hatası: {e}")
            return False
            
    def get_data_info(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Veri hakkında bilgi döndürür
        
        Args:
            data (pd.DataFrame): Analiz edilecek veri
            
        Returns:
            Dict[str, Any]: Veri bilgileri
        """
        try:
            info = {
                'shape': data.shape,
                'columns': list(data.columns),
                'dtypes': data.dtypes.to_dict(),
                'missing_values': data.isnull().sum().to_dict(),
                'descriptive_stats': data.describe().to_dict()
            }
            
            self.logger.info("Veri bilgileri başarıyla oluşturuldu")
            return info
            
        except Exception as e:
            self.logger.error(f"Veri bilgisi oluşturma hatası: {e}")
            return {}
