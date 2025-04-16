import matplotlib.pyplot as plt
from vector.data_operations import create_sample_data
from http_requests.requests_handler import RequestsHandler

# Örnek veri oluşturma
df = create_sample_data(func='cos')

# Basit bir grafik çizme
plt.plot(df['x'], df['y'], label='Kosinüs Fonksiyonu', color='orange')
plt.title('Kosinüs Fonksiyonu Grafiği')
plt.xlabel('X Değeri')
plt.ylabel('Y Değeri')
plt.legend()
plt.grid()
plt.show()

# POST isteği yapma
data_to_send = {'key': 'value'}  # Gönderilecek veri
response = RequestsHandler.post_request('https://api.example.com/data', data_to_send)
