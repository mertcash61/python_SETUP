using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace android.cs
{
    public class Settings
    {
        // Kullanıcının en son kullandığı hesaplama türü
        public string LastUsedCalculationType { get; set; }
        
        // Kullanıcının en son girdiği sayı
        public int LastInputNumber { get; set; }

        // Kullanıcının tercih ettiği tema (örneğin, "Karanlık" veya "Aydınlık")
        public string PreferredTheme { get; set; }

        // Uygulamanın en son açılış tarihi
        public DateTime LastOpened { get; set; }

        // Kullanıcının hesaplama sonuçlarını saklamak için bir liste
        public List<string> CalculationHistory { get; set; }

        public Settings()
        {
            // Varsayılan değerler
            LastUsedCalculationType = "Factorial"; // Varsayılan hesaplama türü
            LastInputNumber = 0; // Varsayılan giriş numarası
            PreferredTheme = "Aydınlık"; // Varsayılan tema
            LastOpened = DateTime.Now; // Uygulama ilk açıldığında tarih
            CalculationHistory = new List<string>(); // Hesaplama geçmişi
        }

        // Kullanıcı giriş bilgilerini güncelleyen metot
        public void UpdateUserInput(int inputNumber, string calculationType)
        {
            LastInputNumber = inputNumber; // Kullanıcının girdiği sayıyı güncelle
            LastUsedCalculationType = calculationType; // Kullanıcının kullandığı hesaplama türünü güncelle
            LastOpened = DateTime.Now; // Uygulamanın en son açılış tarihini güncelle
            CalculationHistory.Add($"Giriş: {inputNumber}, Hesaplama Türü: {calculationType}"); // Hesaplama geçmişine ekle
        }

        // Kullanıcı ayarlarını sıfırlayan metot
        public void ResetSettings()
        {
            LastUsedCalculationType = "Factorial"; // Varsayılan hesaplama türü
            LastInputNumber = 0; // Varsayılan giriş numarası
            PreferredTheme = "Aydınlık"; // Varsayılan tema
            LastOpened = DateTime.Now; // Uygulama ilk açıldığında tarih
            CalculationHistory.Clear(); // Hesaplama geçmişini temizle
        }

        // Diğer ayarları ekleyebilirsiniz
    }
}