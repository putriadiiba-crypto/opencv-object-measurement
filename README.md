# OpenCV Real-Time Object Measurement

Aplikasi pengukuran dimensi objek (panjang & lebar) secara *real-time* menggunakan visi komputer (OpenCV). Aplikasi ini dirancang untuk mendeteksi Kartu SIM (standar 8.5 cm) sebagai objek referensi untuk mengkalibrasi rasio piksel ke ukuran fisik dunia nyata secara dinamis. 

Mendukung penggunaan **Apple Continuity Camera** (iPhone sebagai *webcam* Mac) untuk kualitas pembacaan yang lebih tajam.

## Fitur Utama
- **Kalibrasi Referensi Otomatis:** Otomatis mendeteksi objek paling kiri sebagai Kartu SIM referensi (8.5 cm).
- **Standarisasi Jarak Kamera:** Memberikan panduan teks *real-time* di layar ("Terlalu Dekat", "Terlalu Jauh", "JARAK KAMERA PAS") untuk memastikan akurasi pengukuran.
- **Konversi Multi-Satuan:** Menampilkan ukuran dalam Centimeter (cm), Milimeter (mm), atau Inci (inch) yang bisa diubah kapan saja.
- **Stabilizer Pengukuran:** Menerapkan *Exponential Moving Average* untuk meredam loncatan angka agar hasil ukuran tidak berkedip (*jittering*).

## Persyaratan Sistem
- Python 3.x
- macOS (Direkomendasikan menggunakan iPhone Continuity Camera)

## Instalasi
1. *Clone* atau unduh repositori ini.
2. Buat dan aktifkan *virtual environment*:
   ```bash
   python3 -m venv venv
   source venv/bin/activate