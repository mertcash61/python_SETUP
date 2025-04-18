using System;
using System.Windows.Forms;

namespace android.cs
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
            Application.Run(new Form1());
        }
    }
}
