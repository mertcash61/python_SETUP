document.addEventListener('DOMContentLoaded', function() {
    console.log("Setup Uygulaması Başlatıldı");
    
    // Sekme değiştirme fonksiyonu
    function switchTab(tabId) {
        // Tüm sekme içeriklerini gizle
        const allContents = document.querySelectorAll('.tab-content');
        allContents.forEach(content => {
            content.classList.remove('active');
        });
        
        // Tüm sekme butonlarını inaktif yap
        const allButtons = document.querySelectorAll('.tab-button');
        allButtons.forEach(button => {
            button.classList.remove('active');
        });
        
        // Seçilen sekmeyi ve içeriğini aktif yap
        document.getElementById(tabId).classList.add('active');
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
        
        // İlerleme çubuğunu güncelle
        updateProgressBar(tabId);
    }
    
    // İlerleme çubuğunu güncelleme
    function updateProgressBar(tabId) {
        const progressBar = document.querySelector('.progress');
        
        switch(tabId) {
            case 'general':
                progressBar.style.width = '33%';
                break;
            case 'connection':
                progressBar.style.width = '66%';
                break;
            case 'advanced':
                progressBar.style.width = '100%';
                break;
        }
    }
    
    // Sekme butonlarına tıklama olaylarını ekle
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            switchTab(tabId);
        });
    });
    
    // İleri butonlarına tıklama olaylarını ekle
    const nextButtons = document.querySelectorAll('.next-button');
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const nextTabId = this.getAttribute('data-next');
            switchTab(nextTabId);
        });
    });
    
    // Geri butonlarına tıklama olaylarını ekle
    const prevButtons = document.querySelectorAll('.prev-button');
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const prevTabId = this.getAttribute('data-prev');
            switchTab(prevTabId);
        });
    });
    
    // Form doğrulama fonksiyonu
    function validateForm(formId) {
        const form = document.getElementById(formId);
        let isValid = true;
        
        // Gerekli alanları kontrol et
        const requiredInputs = form.querySelectorAll('[required]');
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.style.borderColor = 'var(--error-color)';
                isValid = false;
                
                // Focus ve scroll
                if (isValid === false) {
                    input.focus();
                    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            } else {
                input.style.borderColor = 'var(--border-color)';
            }
        });
        
        return isValid;
    }
    
    // Tüm ayarları toplama
    function collectAllSettings() {
        const settings = {};
        
        // Genel ayarlar
        settings.appName = document.getElementById('appName').value;
        settings.language = document.getElementById('language').value;
        settings.theme = document.querySelector('input[name="theme"]:checked').value;
        
        // Bağlantı ayarları
        settings.apiUrl = document.getElementById('apiUrl').value;
        settings.timeout = parseInt(document.getElementById('timeout').value);
        settings.retryAttempts = parseInt(document.getElementById('retryAttempts').value);
        
        // Gelişmiş ayarlar
        settings.logLevel = document.getElementById('logLevel').value;
        settings.cacheSize = parseInt(document.getElementById('cacheSize').value);
        settings.enableNotifications = document.getElementById('enableNotifications').checked;
        settings.enableAutoUpdate = document.getElementById('enableAutoUpdate').checked;
        
        return settings;
    }
    
    // Ayarları kaydetme
    async function saveSettings(settings) {
        try {
            console.log("Kaydedilecek ayarlar:", settings);
            
            // Gerçek API isteği (gerçek projede bu kısmı API URL'si ile değiştirin)
            const response = await fetch('https://api.example.com/save_settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });
            
            if (!response.ok) {
                throw new Error('Ayarları kaydederken bir hata oluştu.');
            }
            
            const result = await response.json();
            showFeedback(result.message, true);
        } catch (error) {
            showFeedback(error.message, false);
        }
    }
    
    // Geri bildirim gösterme
    function showFeedback(message, isSuccess = true) {
        const feedback = document.getElementById('feedback');
        const feedbackText = document.getElementById('feedbackText');
        
        feedbackText.textContent = message;
        feedback.style.display = 'flex';
        
        if (isSuccess) {
            feedback.style.backgroundColor = '#e6f4ea';
            feedback.style.color = 'var(--success-color)';
        } else {
            feedback.style.backgroundColor = '#fce8e6';
            feedback.style.color = 'var(--error-color)';
        }
        
        // 5 saniye sonra geri bildirimi gizle
        setTimeout(() => {
            feedback.style.display = 'none';
        }, 5000);
    }
    
    // Kaydet butonuna tıklama olayını ekle
    document.getElementById('saveButton').addEventListener('click', function() {
        // Formu doğrula
        if (!validateForm('advancedForm')) {
            showFeedback("Lütfen tüm gerekli alanları doldurun.", false);
            return;
        }
        
        // Tüm ayarları topla
        const settings = collectAllSettings();
        
        // Kaydetme animasyonu
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Kaydediliyor...';
        
        // Ayarları kaydet
        saveSettings(settings)
            .finally(() => {
                // Butonu eski haline getir
                this.disabled = false;
                this.innerHTML = 'Ayarları Kaydet <i class="fas fa-save"></i>';
            });
    });
    
    // Tema değişikliğini uygula
    document.querySelectorAll('input[name="theme"]').forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'dark') {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }
        });
    });
    
    // Input doğrulaması için olay dinleyiciler
    document.querySelectorAll('input[required]').forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.style.borderColor = 'var(--border-color)';
            }
        });
    });
});
