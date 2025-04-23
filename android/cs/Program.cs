using System;
using System.Windows.Forms;

namespace YourNamespace // Uygulamanızın ad alanını buraya ekleyin
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            // Windows Forms uygulaması için gerekli ayarları yap
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            
            // Ana formu başlat
            Application.Run(new Form1()); // Form1, kullanıcı giriş kaydı ve faktöriyel hesaplama içeren form
        }
    }
}
