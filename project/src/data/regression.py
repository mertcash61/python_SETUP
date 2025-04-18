import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, Any, Tuple, List
import logging
from pathlib import Path
import joblib

class RegressionAnalysis:
    """
    Regresyon analizi için sınıf.
    
    Bu sınıf, doğrusal regresyon, ridge regresyon ve lasso regresyon
    modellerini uygular ve değerlendirir.
    """
    
    def __init__(self):
        """RegressionAnalysis sınıfı başlatıcısı"""
        # Loglama ayarları
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "regression.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def prepare_data(
        self,
        data: pd.DataFrame,
        target_column: str,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Veriyi eğitim ve test setlerine ayırır
        
        Args:
            data (pd.DataFrame): Veri seti
            target_column (str): Hedef değişken adı
            test_size (float): Test seti oranı
            random_state (int): Rastgele durum
            
        Returns:
            Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Eğitim ve test setleri
        """
        try:
            X = data.drop(columns=[target_column])
            y = data[target_column]
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state
            )
            
            self.logger.info("Veri başarıyla hazırlandı")
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            self.logger.error(f"Veri hazırlama hatası: {e}")
            raise
            
    def train_linear_regression(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray
    ) -> Tuple[LinearRegression, Dict[str, Any]]:
        """
        Doğrusal regresyon modelini eğitir
        
        Args:
            X_train (np.ndarray): Eğitim verisi
            y_train (np.ndarray): Eğitim hedefi
            
        Returns:
            Tuple[LinearRegression, Dict[str, Any]]: Model ve metrikler
        """
        try:
            model = LinearRegression()
            model.fit(X_train, y_train)
            
            metrics = {
                'coefficients': model.coef_.tolist(),
                'intercept': model.intercept_,
                'score': model.score(X_train, y_train)
            }
            
            self.logger.info("Doğrusal regresyon modeli başarıyla eğitildi")
            return model, metrics
            
        except Exception as e:
            self.logger.error(f"Doğrusal regresyon eğitim hatası: {e}")
            raise
            
    def train_ridge_regression(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        alpha: float = 1.0
    ) -> Tuple[Ridge, Dict[str, Any]]:
        """
        Ridge regresyon modelini eğitir
        
        Args:
            X_train (np.ndarray): Eğitim verisi
            y_train (np.ndarray): Eğitim hedefi
            alpha (float): Regularizasyon parametresi
            
        Returns:
            Tuple[Ridge, Dict[str, Any]]: Model ve metrikler
        """
        try:
            model = Ridge(alpha=alpha)
            model.fit(X_train, y_train)
            
            metrics = {
                'coefficients': model.coef_.tolist(),
                'intercept': model.intercept_,
                'score': model.score(X_train, y_train)
            }
            
            self.logger.info("Ridge regresyon modeli başarıyla eğitildi")
            return model, metrics
            
        except Exception as e:
            self.logger.error(f"Ridge regresyon eğitim hatası: {e}")
            raise
            
    def train_lasso_regression(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        alpha: float = 1.0
    ) -> Tuple[Lasso, Dict[str, Any]]:
        """
        Lasso regresyon modelini eğitir
        
        Args:
            X_train (np.ndarray): Eğitim verisi
            y_train (np.ndarray): Eğitim hedefi
            alpha (float): Regularizasyon parametresi
            
        Returns:
            Tuple[Lasso, Dict[str, Any]]: Model ve metrikler
        """
        try:
            model = Lasso(alpha=alpha)
            model.fit(X_train, y_train)
            
            metrics = {
                'coefficients': model.coef_.tolist(),
                'intercept': model.intercept_,
                'score': model.score(X_train, y_train)
            }
            
            self.logger.info("Lasso regresyon modeli başarıyla eğitildi")
            return model, metrics
            
        except Exception as e:
            self.logger.error(f"Lasso regresyon eğitim hatası: {e}")
            raise
            
    def evaluate_model(
        self,
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict[str, float]:
        """
        Model performansını değerlendirir
        
        Args:
            model (Any): Eğitilmiş model
            X_test (np.ndarray): Test verisi
            y_test (np.ndarray): Test hedefi
            
        Returns:
            Dict[str, float]: Değerlendirme metrikleri
        """
        try:
            y_pred = model.predict(X_test)
            
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2': r2_score(y_test, y_pred)
            }
            
            self.logger.info("Model başarıyla değerlendirildi")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Model değerlendirme hatası: {e}")
            raise
            
    def save_model(self, model: Any, file_path: str) -> bool:
        """
        Modeli kaydeder
        
        Args:
            model (Any): Kaydedilecek model
            file_path (str): Kayıt yolu
            
        Returns:
            bool: İşlem başarılı ise True
        """
        try:
            joblib.dump(model, file_path)
            self.logger.info(f"Model başarıyla kaydedildi: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Model kaydetme hatası: {e}")
            return False
            
    def load_model(self, file_path: str) -> Any:
        """
        Modeli yükler
        
        Args:
            file_path (str): Model dosyası yolu
            
        Returns:
            Any: Yüklenen model
        """
        try:
            model = joblib.load(file_path)
            self.logger.info(f"Model başarıyla yüklendi: {file_path}")
            return model
            
        except Exception as e:
            self.logger.error(f"Model yükleme hatası: {e}")
            raise
