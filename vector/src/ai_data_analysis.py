import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import json  # JSON dosyası ile çalışmak için

class AIDataAnalysis:
    """Yapay zeka destekli veri analizi için sınıf."""

    @staticmethod
    def perform_regression_analysis(df):
        """Veri çerçevesi üzerinde basit regresyon analizi yapma."""
        X = df[['x']]  # Bağımsız değişken
        y = df['y']    # Bağımlı değişken

        model = LinearRegression()
        model.fit(X, y)

        # Regresyon sonuçlarını yazdırma
        print("Katsayılar:", model.coef_)
        print("Sabit terim:", model.intercept_)

        # Tahmin yapma
        predictions = model.predict(X)

        # Sonuçları görselleştirme
        plt.scatter(X, y, color='blue', label='Gerçek Veriler')
        plt.plot(X, predictions, color='red', label='Regresyon Doğrusu')
        plt.title('Basit Regresyon Analizi')
        plt.xlabel('X Değeri')
        plt.ylabel('Y Değeri')
        plt.legend()
        plt.grid()
        plt.show()

        # Regresyon sonuçlarını kaydetme
        results = {
            "coefficients": model.coef_.tolist(),
            "intercept": model.intercept_.tolist()
        }
        AIDataAnalysis.save_results(results)

    @staticmethod
    def analyze_data(df):
        """Veri analizi yapma."""
        print("Veri Özeti:")
        print(df.describe())
        print("\nKorelasyon Matrisi:")
        print(df.corr())

    @staticmethod
    def save_results(results):
        """Regresyon sonuçlarını JSON dosyasına kaydetme."""
        with open('regression_results.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)
        print("Regresyon sonuçları 'regression_results.json' dosyasına kaydedildi.")
