// Sistem Gereksinimleri:
// 1. .NET Framework 4.5 veya üzeri
// 2. Windows Forms uygulaması için gerekli bileşenler
// 3. Kullanıcıdan pozitif tam sayı girişi alabilme
// 4. Hesaplama işlemleri için yeterli bellek

using System;
using System.Windows.Forms;

namespace android.cs
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // ComboBox'a hesaplama türlerini ekleyin
            comboBoxCalculationType.Items.AddRange(Enum.GetNames(typeof(EnumController)));
        }

        private void btnCalculate_Click(object sender, EventArgs e)
        {
            if (int.TryParse(txtInput.Text, out int n) && n >= 0) // Kullanıcıdan sayı al
            {
                long result = Factorial(n); // Faktöriyel hesapla
                lblResult.Text = $"Faktöriyel: {result}"; // Sonucu göster
            }
            else
            {
                MessageBox.Show("Lütfen geçerli bir pozitif tam sayı girin."); // Hata mesajı
            }
        }

        // Faktöriyel hesaplama metodu (while döngüsü ile)
        private long Factorial(int n)
        {
            long result = 1;
            int i = 2; // Başlangıç değeri
            while (i <= n)
            {
                result *= i; // Sonucu güncelle
                i++; // Artır
            }
            return result;
        }
    }
}