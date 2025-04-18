import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path
from .data_operations import DataOperations
from .regression import RegressionAnalysis
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import json

class AIAnalysis:
    """
    Yapay zeka analizi için ana sınıf.
    
    Bu sınıf, veri analizi, kümeleme ve boyut indirgeme işlemlerini
    yönetir ve görselleştirme sağlar.
    """
    
    def __init__(self):
        """AIAnalysis sınıfı başlatıcısı"""
        # Loglama ayarları
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "ai_analysis.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Alt sınıfları başlat
        self.data_ops = DataOperations()
        self.regression = RegressionAnalysis()
        
    def analyze_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Veriyi analiz eder
        
        Args:
            data (pd.DataFrame): Analiz edilecek veri
            
        Returns:
            Dict[str, Any]: Analiz sonuçları
        """
        try:
            # Temel istatistikler
            stats = data.describe().to_dict()
            
            # Korelasyon analizi
            corr = data.corr().to_dict()
            
            # Eksik değer analizi
            missing = data.isnull().sum().to_dict()
            
            # Aykırı değer analizi
            outliers = {}
            for col in data.select_dtypes(include=[np.number]).columns:
                Q1 = data[col].quantile(0.25)
                Q3 = data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers[col] = len(data[(data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR))])
                
            results = {
                'statistics': stats,
                'correlation': corr,
                'missing_values': missing,
                'outliers': outliers
            }
            
            self.logger.info("Veri analizi başarıyla tamamlandı")
            return results
            
        except Exception as e:
            self.logger.error(f"Veri analizi hatası: {e}")
            raise
            
    def perform_clustering(
        self,
        data: pd.DataFrame,
        method: str = 'kmeans',
        n_clusters: int = 3,
        eps: float = 0.5,
        min_samples: int = 5
    ) -> Dict[str, Any]:
        """
        Kümeleme analizi yapar
        
        Args:
            data (pd.DataFrame): Kümeleme yapılacak veri
            method (str): Kümeleme metodu (kmeans, dbscan)
            n_clusters (int): Küme sayısı (kmeans için)
            eps (float): Maksimum mesafe (dbscan için)
            min_samples (int): Minimum örnek sayısı (dbscan için)
            
        Returns:
            Dict[str, Any]: Kümeleme sonuçları
        """
        try:
            # Veriyi ölçeklendir
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            if method == 'kmeans':
                model = KMeans(n_clusters=n_clusters, random_state=42)
            elif method == 'dbscan':
                model = DBSCAN(eps=eps, min_samples=min_samples)
            else:
                raise ValueError(f"Desteklenmeyen kümeleme metodu: {method}")
                
            # Kümeleme yap
            clusters = model.fit_predict(scaled_data)
            
            # Sonuçları hazırla
            results = {
                'labels': clusters.tolist(),
                'n_clusters': len(np.unique(clusters)),
                'method': method
            }
            
            if method == 'kmeans':
                results['centers'] = model.cluster_centers_.tolist()
                results['inertia'] = model.inertia_
                
            self.logger.info(f"{method} kümeleme analizi başarıyla tamamlandı")
            return results
            
        except Exception as e:
            self.logger.error(f"Kümeleme analizi hatası: {e}")
            raise
            
    def perform_pca(
        self,
        data: pd.DataFrame,
        n_components: int = 2
    ) -> Dict[str, Any]:
        """
        Temel bileşen analizi yapar
        
        Args:
            data (pd.DataFrame): Analiz edilecek veri
            n_components (int): Bileşen sayısı
            
        Returns:
            Dict[str, Any]: PCA sonuçları
        """
        try:
            # Veriyi ölçeklendir
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)
            
            # PCA uygula
            pca = PCA(n_components=n_components)
            components = pca.fit_transform(scaled_data)
            
            # Sonuçları hazırla
            results = {
                'components': components.tolist(),
                'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
                'explained_variance': pca.explained_variance_.tolist()
            }
            
            self.logger.info("PCA analizi başarıyla tamamlandı")
            return results
            
        except Exception as e:
            self.logger.error(f"PCA analizi hatası: {e}")
            raise
            
    def visualize_results(
        self,
        data: pd.DataFrame,
        results: Dict[str, Any],
        output_path: str
    ) -> bool:
        """
        Analiz sonuçlarını görselleştirir
        
        Args:
            data (pd.DataFrame): Veri seti
            results (Dict[str, Any]): Analiz sonuçları
            output_path (str): Çıktı dosyası yolu
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            # Korelasyon matrisi
            plt.figure(figsize=(10, 8))
            sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
            plt.title('Korelasyon Matrisi')
            plt.savefig(f"{output_path}/correlation_matrix.png")
            plt.close()
            
            # Kümeleme sonuçları
            if 'labels' in results:
                plt.figure(figsize=(10, 8))
                plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=results['labels'])
                plt.title('Kümeleme Sonuçları')
                plt.savefig(f"{output_path}/clustering_results.png")
                plt.close()
                
            # PCA sonuçları
            if 'components' in results:
                plt.figure(figsize=(10, 8))
                plt.scatter(results['components'][:, 0], results['components'][:, 1])
                plt.title('PCA Sonuçları')
                plt.savefig(f"{output_path}/pca_results.png")
                plt.close()
                
            self.logger.info(f"Görselleştirmeler başarıyla kaydedildi: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Görselleştirme hatası: {e}")
            return False
            
    def generate_report(
        self,
        data: pd.DataFrame,
        results: Dict[str, Any],
        output_path: str
    ) -> bool:
        """
        Analiz raporu oluşturur
        
        Args:
            data (pd.DataFrame): Veri seti
            results (Dict[str, Any]): Analiz sonuçları
            output_path (str): Çıktı dosyası yolu
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            report = {
                'data_info': self.data_ops.get_data_info(data),
                'analysis_results': results,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            # Raporu kaydet
            with open(f"{output_path}/analysis_report.json", 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
                
            self.logger.info(f"Rapor başarıyla oluşturuldu: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Rapor oluşturma hatası: {e}")
            return False
