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
            // Kullanıcıdan girdi alma
            if (int.TryParse(txtInput.Text, out int number) && number >= 0)
            {
                // Hesaplamaları yapma
                long factorial = Factorial(number);
                int square = number * number;
                int cube = number * number * number;

                // Seçilen hesaplama türüne göre sonuçları gösterme
                string calculationType = comboBoxCalculationType.SelectedItem.ToString();
                string resultMessage = $"Girdiğiniz sayı: {number}\n";

                switch (calculationType)
                {
                    case nameof(EnumController.Factorial):
                        resultMessage += $"Sayının faktöriyeli: {factorial}";
                        break;
                    case nameof(EnumController.Square):
                        resultMessage += $"Sayının karesi: {square}";
                        break;
                    case nameof(EnumController.Cube):
                        resultMessage += $"Sayının küpü: {cube}";
                        break;
                }

                lblResult.Text = resultMessage;
            }
            else
            {
                // Geçersiz girdi durumu
                MessageBox.Show("Geçersiz bir sayı girdiniz. Lütfen pozitif bir tam sayı girin.", "Hata", MessageBoxButtons.OK, MessageBoxIcon.Error);
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