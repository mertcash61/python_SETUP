import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class RegressionAnalysis:
    """Yapay zeka destekli regresyon analizi için sınıf."""

    @staticmethod
    def load_data(file_path):
        """Veri yükleme."""
        df = pd.read_csv(file_path)
        print("Veri yüklendi:")
        print(df.head())
        return df

    @staticmethod
    def preprocess_data(df):
        """Veri ön işleme."""
        # Gerekli ön işleme adımları burada yapılabilir
        # Örneğin, eksik verileri doldurma veya normalizasyon
        return df

    @staticmethod
    def perform_regression_analysis(df):
        """Veri çerçevesi üzerinde regresyon analizi yapma."""
        X = df[['x']]  # Bağımsız değişken
        y = df['y']    # Bağımlı değişken

        # Veriyi eğitim ve test setlerine ayırma
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        # Regresyon sonuçlarını yazdırma
        print("Katsayılar:", model.coef_)
        print("Sabit terim:", model.intercept_)

        # Tahmin yapma
        predictions = model.predict(X_test)

        # Sonuçları görselleştirme
        plt.scatter(X_test, y_test, color='blue', label='Gerçek Veriler')
        plt.plot(X_test, predictions, color='red', label='Regresyon Doğrusu')
        plt.title('Regresyon Analizi')
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
