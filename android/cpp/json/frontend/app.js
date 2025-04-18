document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript Android Uygulaması");

    // Örnek veri (gerçek verilerle değiştirin)
    const data = [
        { x: 1, y: 2 },
        { x: 2, y: 3 },
        { x: 3, y: 5 },
        { x: 4, y: 7 },
        { x: 5, y: 11 }
    ];

    // Regresyon analizi fonksiyonu
    function performRegression(data) {
        const n = data.length;  // Veri sayısını al
        const sumX = data.reduce((sum, point) => sum + point.x, 0);  // x değerlerinin toplamı
        const sumY = data.reduce((sum, point) => sum + point.y, 0);  // y değerlerinin toplamı
        const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);  // x * y değerlerinin toplamı
        const sumX2 = data.reduce((sum, point) => sum + point.x * point.x, 0);  // x^2 değerlerinin toplamı

        // Regresyon katsayılarını hesaplama
        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);  // Eğim
        const intercept = (sumY - slope * sumX) / n;  // Kesişim

        return { slope, intercept };  // Sonuçları döndür
    }

    // Regresyon sonuçlarını kaydetme
    function saveResults(results) {
        console.log("Regresyon Sonuçları:", results);
        
        // Örnek API isteği (gerçek URL ile değiştirin)
        fetch('https://api.example.com/save_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(results)  // Sonuçları JSON formatında gönder
        })
        .then(response => response.json())
        .then(data => {
            console.log("Sonuçlar başarıyla kaydedildi:", data);
            // Geri bildirim mesajını göster
            const feedback = document.getElementById('feedback');
            feedback.style.display = 'block';
            feedback.textContent = "Ayarlar başarıyla kaydedildi!";
        })
        .catch(error => {
            console.error("Sonuçlar kaydedilirken bir hata oluştu:", error);
            // Hata durumunda geri bildirim mesajını göster
            const feedback = document.getElementById('feedback');
            feedback.style.display = 'block';
            feedback.textContent = "Ayarlar kaydedilirken bir hata oluştu.";
        });
    }

    // Ayarları JSON olarak kaydetme
    document.getElementById('saveButton').addEventListener('click', function() {
        const apiUrl = document.getElementById('apiUrl').value;  // API URL'sini al
        const settings = {
            apiUrl: apiUrl,
            timeout: 30,  // Örnek ayar
            retryAttempts: 3  // Örnek ayar
        };
        saveResults(settings);  // Ayarları kaydet
    });

    // Regresyon analizi yapma ve sonuçları kaydetme
    const regressionResults = performRegression(data);  // Regresyon analizi yap
    saveResults(regressionResults);  // Sonuçları kaydet
});
