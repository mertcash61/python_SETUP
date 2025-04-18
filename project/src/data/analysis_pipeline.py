import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
import logging
from pathlib import Path
from .data_operations import DataOperations
from .regression import RegressionAnalysis
from .ai_analysis import AIAnalysis

class AnalysisPipeline:
    """
    Veri analizi pipeline'ı için ana sınıf.
    
    Bu sınıf, veri işleme, regresyon analizi ve yapay zeka analizi
    işlemlerini bir arada yönetir.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        AnalysisPipeline sınıfı başlatıcısı
        
        Args:
            config (Dict[str, Any]): Pipeline yapılandırması
        """
        self.config = config
        
        # Loglama ayarları
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "analysis_pipeline.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Alt sınıfları başlat
        self.data_ops = DataOperations()
        self.regression = RegressionAnalysis()
        self.ai_analysis = AIAnalysis()
        
    def run_pipeline(self, data_path: str) -> Dict[str, Any]:
        """
        Analiz pipeline'ını çalıştırır
        
        Args:
            data_path (str): Veri dosyası yolu
            
        Returns:
            Dict[str, Any]: Analiz sonuçları
        """
        try:
            results = {}
            
            # 1. Veri yükleme
            self.logger.info("Veri yükleniyor...")
            data = self.data_ops.load_data(data_path)
            if data is None:
                raise ValueError("Veri yüklenemedi")
                
            # 2. Veri temizleme
            self.logger.info("Veri temizleniyor...")
            data = self.data_ops.clean_data(data, self.config['cleaning'])
            
            # 3. Veri normalizasyonu
            self.logger.info("Veri normalize ediliyor...")
            data = self.data_ops.normalize_data(data, self.config['normalization']['method'])
            
            # 4. Veri analizi
            self.logger.info("Veri analizi yapılıyor...")
            analysis_results = self.ai_analysis.analyze_data(data)
            results['analysis'] = analysis_results
            
            # 5. Kümeleme analizi
            if self.config['clustering']['enabled']:
                self.logger.info("Kümeleme analizi yapılıyor...")
                clustering_results = self.ai_analysis.perform_clustering(
                    data,
                    method=self.config['clustering']['method'],
                    n_clusters=self.config['clustering']['n_clusters']
                )
                results['clustering'] = clustering_results
                
            # 6. PCA analizi
            if self.config['pca']['enabled']:
                self.logger.info("PCA analizi yapılıyor...")
                pca_results = self.ai_analysis.perform_pca(
                    data,
                    n_components=self.config['pca']['n_components']
                )
                results['pca'] = pca_results
                
            # 7. Regresyon analizi
            if self.config['regression']['enabled']:
                self.logger.info("Regresyon analizi yapılıyor...")
                X_train, X_test, y_train, y_test = self.regression.prepare_data(
                    data,
                    self.config['regression']['target_column'],
                    test_size=self.config['regression']['test_size']
                )
                
                # Doğrusal regresyon
                linear_model, linear_metrics = self.regression.train_linear_regression(X_train, y_train)
                linear_eval = self.regression.evaluate_model(linear_model, X_test, y_test)
                results['regression']['linear'] = {
                    'metrics': linear_metrics,
                    'evaluation': linear_eval
                }
                
                # Ridge regresyon
                ridge_model, ridge_metrics = self.regression.train_ridge_regression(
                    X_train,
                    y_train,
                    alpha=self.config['regression']['ridge_alpha']
                )
                ridge_eval = self.regression.evaluate_model(ridge_model, X_test, y_test)
                results['regression']['ridge'] = {
                    'metrics': ridge_metrics,
                    'evaluation': ridge_eval
                }
                
                # Lasso regresyon
                lasso_model, lasso_metrics = self.regression.train_lasso_regression(
                    X_train,
                    y_train,
                    alpha=self.config['regression']['lasso_alpha']
                )
                lasso_eval = self.regression.evaluate_model(lasso_model, X_test, y_test)
                results['regression']['lasso'] = {
                    'metrics': lasso_metrics,
                    'evaluation': lasso_eval
                }
                
            # 8. Görselleştirme
            self.logger.info("Sonuçlar görselleştiriliyor...")
            self.ai_analysis.visualize_results(data, results, self.config['output_path'])
            
            # 9. Rapor oluşturma
            self.logger.info("Rapor oluşturuluyor...")
            self.ai_analysis.generate_report(data, results, self.config['output_path'])
            
            self.logger.info("Pipeline başarıyla tamamlandı")
            return results
            
        except Exception as e:
            self.logger.error(f"Pipeline hatası: {e}")
            raise
            
    def save_results(self, results: Dict[str, Any], output_path: str) -> bool:
        """
        Analiz sonuçlarını kaydeder
        
        Args:
            results (Dict[str, Any]): Kaydedilecek sonuçlar
            output_path (str): Kayıt yolu
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            # Sonuçları JSON olarak kaydet
            import json
            with open(f"{output_path}/results.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
                
            # Modelleri kaydet
            if 'regression' in results:
                for model_name, model_data in results['regression'].items():
                    model_path = f"{output_path}/{model_name}_model.joblib"
                    self.regression.save_model(model_data['model'], model_path)
                    
            self.logger.info(f"Sonuçlar başarıyla kaydedildi: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Sonuç kaydetme hatası: {e}")
            return False 