import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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

    @staticmethod
    def analyze_data(df):
        """Veri analizi yapma."""
        print("Veri Özeti:")
        print(df.describe())
        print("\nKorelasyon Matrisi:")
        print(df.corr())
