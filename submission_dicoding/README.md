# 🚲 Bike Sharing Data Analytics Dashboard ✨

Ini adalah proyek akhir dari kursus Dicoding "Belajar Analisis Data dengan Python" untuk melakukan analisis data pada Bike Sharing Dataset. Dashboard ini dibuat menggunakan Streamlit untuk memvisualisasikan tren penyewaan sepeda berdasarkan berbagai faktor seperti cuaca, musim, dan tipe pengguna.

## 📂 Struktur Direktori
- **dashboard/**: Berisi file utama dashboard (`dashboard.py`) dan dataset yang sudah dibersihkan (`main_data.csv`).
- **data/**: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- **Proyek_Analisis_Data.ipynb**: File notebook untuk analisis data lengkap (Wrangling, EDA, Visualization).
- **requirements.txt**: Daftar library Python yang diperlukan untuk menjalankan proyek.
- **README.md**: Dokumentasi proyek.
- **url.txt**: Berisi link dashboard yang telah di-deploy.

## 🛠️ Setup Environment - Anaconda
Jika Anda menggunakan Anaconda, ikuti langkah berikut untuk menyiapkan lingkungan:
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## 💻 Setup Environment - Shell/Terminal
Jika Anda menggunakan terminal biasa (CMD/PowerShell/Bash), ikuti langkah berikut:
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 🚀 Menjalankan Dashboard Secara Lokal
Untuk menjalankan dashboard di komputer lokal, pastikan Anda berada di direktori utama proyek, lalu jalankan perintah berikut:
```bash
cd dashboard
streamlit run dashboard.py
```

## 🌐 Dashboard URL
Aplikasi dashboard ini telah di-deploy dan dapat diakses secara online melalui link berikut:
[https://bike-sharing-dashboard-dicoding2026.streamlit.app/](https://bike-sharing-dashboard-dicoding2026.streamlit.app/)

---
**Informasi Kontak:**
- **Nama:** Ning Ayu Lailatul Maghfiroh
- **Email:** CDCC487D6X1760@student.devacademy.id
- **ID Dicoding:** CDCC487D6X1760