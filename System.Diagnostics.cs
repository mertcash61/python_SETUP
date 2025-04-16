using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        // Python betiğini çalıştır
        ProcessStartInfo start = new ProcessStartInfo();
        start.FileName = "python"; // Python'un yüklü olduğu yolu belirtin
        start.Arguments = "path/to/your/python_script.py"; // Python betiğinizin yolu
        start.UseShellExecute = false;
        start.RedirectStandardOutput = true;
        start.RedirectStandardError = true;

        using (Process process = Process.Start(start))
        {
            using (System.IO.StreamReader reader = process.StandardOutput)
            {
                string result = reader.ReadToEnd();
                Console.WriteLine(result); // Python çıktısını yazdır
            }
        }
    }
}
