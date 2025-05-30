// app.js
document.addEventListener('DOMContentLoaded', function() {
    console.log("Setup Uygulaması Başlatıldı");
    
    // Sayfa yüklendiğinde temayı kontrol et
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    // Tema değişikliğini uygula
    document.querySelectorAll('input[name="theme"]').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'dark') {
                localStorage.setItem('theme', 'dark'); // Temayı yerel depolamada sakla
                document.body.classList.add('dark-mode');
            } else {
                localStorage.setItem('theme', 'light'); // Temayı yerel depolamada sakla
                document.body.classList.remove('dark-mode');
            }
        });
    });

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
        const n = data.length;
        const sumX = data.reduce((sum, point) => sum + point.x, 0);
        const sumY = data.reduce((sum, point) => sum + point.y, 0);
        const sumXY = data.reduce((sum, point) => sum + point.x * point.y, 0);
        const sumX2 = data.reduce((sum, point) => sum + point.x * point.x, 0);

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;

        return { slope, intercept };
    }

    // Regresyon sonuçlarını kaydetme
    async function saveResults(results) {
        try {
            const response = await fetch('https://api.example.com/save_results', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(results)
            });
            const data = await response.json();
            console.log("Sonuçlar başarıyla kaydedildi:", data);
        } catch (error) {
            console.error("Sonuçlar kaydedilirken bir hata oluştu:", error);
        }
    }

    // Regresyon analizi yapma ve sonuçları kaydetme
    const regressionResults = performRegression(data);
    saveResults(regressionResults);
});
