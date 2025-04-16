import matplotlib.pyplot as plt
from vector.data_operations import create_sample_data
from http_requests.requests_handler import RequestsHandler
from vector.src.regression_analysis import RegressionAnalysis
from sklearn.linear_model import LinearRegression

# Örnek veri oluşturma
df = create_sample_data(func='sin')

# Yapay zeka destekli regresyon analizi
RegressionAnalysis.analyze_data(df)
RegressionAnalysis.perform_regression_analysis(df)

# Basit bir grafik çizme
plt.figure(figsize=(12, 6))  # Grafik boyutunu ayarlama

# Sinüs fonksiyonu grafiği
plt.subplot(1, 2, 1)  # 1 satır, 2 sütun, 1. grafik
plt.plot(df['x'], df['y'], label='Sinüs Fonksiyonu', color='blue')
plt.title('Sinüs Fonksiyonu Grafiği')
plt.xlabel('X Değeri')
plt.ylabel('Y Değeri')
plt.legend()
plt.grid()

# Regresyon analizi grafiği
plt.subplot(1, 2, 2)  # 1 satır, 2 sütun, 2. grafik
X = df[['x']]
y = df['y']
model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)
plt.scatter(X, y, color='blue', label='Gerçek Veriler')
plt.plot(X, predictions, color='red', label='Regresyon Doğrusu')
plt.title('Regresyon Analizi')
plt.xlabel('X Değeri')
plt.ylabel('Y Değeri')
plt.legend()
plt.grid()

plt.tight_layout()  # Grafiklerin düzenini ayarlama
plt.show()

# GET isteği yapma
def perform_get_request():
    url = 'https://api.example.com/data'
    data = RequestsHandler.get_request(url)
    if data:
        print("GET isteği sonucu:", data)
    else:
        print("GET isteği başarısız oldu.")

# POST isteği yapma
def perform_post_request():
    url = 'https://api.example.com/data'
    data_to_send = {
        'key1': 'value1',
        'key2': 'value2'
    }
    response = RequestsHandler.post_request(url, data_to_send)
    RequestsHandler.analyze_response(response)

# HTTP isteklerini gerçekleştirme
perform_get_request()
perform_post_request()
