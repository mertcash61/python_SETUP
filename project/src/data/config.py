"""
Veri analizi pipeline'ı için yapılandırma ayarları.
"""

# Temel ayarlar
BASE_CONFIG = {
    'output_path': 'output/analysis',
    
    # Veri temizleme ayarları
    'cleaning': {
        'missing_values': {
            'strategy': 'mean'  # mean, median, mode, drop
        },
        'outliers': {
            'method': 'zscore',  # zscore, iqr
            'threshold': 3
        },
        'categorical': {
            'method': 'onehot',  # onehot, label
            'columns': []
        }
    },
    
    # Normalizasyon ayarları
    'normalization': {
        'method': 'minmax'  # minmax, standard
    },
    
    # Kümeleme ayarları
    'clustering': {
        'enabled': True,
        'method': 'kmeans',  # kmeans, dbscan
        'n_clusters': 3,
        'eps': 0.5,  # DBSCAN için
        'min_samples': 5  # DBSCAN için
    },
    
    # PCA ayarları
    'pca': {
        'enabled': True,
        'n_components': 2
    },
    
    # Regresyon ayarları
    'regression': {
        'enabled': True,
        'target_column': 'target',
        'test_size': 0.2,
        'ridge_alpha': 1.0,
        'lasso_alpha': 1.0
    }
}

# Örnek kullanım:
"""
from project.src.data.analysis_pipeline import AnalysisPipeline
from project.src.data.config import BASE_CONFIG

# Pipeline'ı başlat
pipeline = AnalysisPipeline(BASE_CONFIG)

# Pipeline'ı çalıştır
results = pipeline.run_pipeline('data.csv')

# Sonuçları kaydet
pipeline.save_results(results, BASE_CONFIG['output_path'])
""" 