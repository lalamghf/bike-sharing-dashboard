import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

# ==============================
# CONFIG & STYLE
# ==============================
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid")

# ==============================
# HELPER FUNCTIONS
# ==============================
def create_season_rent_df(df):
    return df.groupby("season")["cnt"].mean().reset_index()

def create_weather_rent_df(df):
    return df.groupby("weathersit")["cnt"].mean().reset_index()

def create_weekday_rent_df(df):
    # Mengelompokkan berdasarkan hari dan tipe pengguna
    weekday_rent_df = df.groupby("weekday")[["casual", "registered"]].mean().reset_index()
    # Pastikan urutan hari benar (0=Minggu, 6=Sabtu atau sesuai dataset Anda)
    return weekday_rent_df

def create_rush_hour_df(df):
    # Filter hanya hari kerja untuk menjawab pertanyaan rush hour
    workingday_df = df[df["workingday"] == 1]
    return workingday_df.groupby("hr")["cnt"].mean().reset_index()

def create_temp_rent_df(df):
    if 'temp_group' in df.columns:
        return df.groupby("temp_group", observed=False)["cnt"].mean().reset_index()
    return None

# ==============================
# LOAD DATA
# ==============================
# Gunakan relative path agar kode bisa jalan di komputer mana saja asal folder dashboard lengkap
try:
    day_df = pd.read_csv("submission_dicoding/dashboard/main_data.csv")
    hour_df = pd.read_csv("submission_dicoding/dashboard/hour.csv")
    
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
except Exception as e:
    st.error(f"Gagal memuat file data. Pastikan main_data.csv dan hour.csv ada di folder yang sama. Error: {e}")
    st.stop()

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    # Menampilkan Gambar Sepeda
    try:
        # Mencari gambar di folder yang sama
        img = Image.open("submission_dicoding/dashboard/sepeda.jpg")
        st.image(img, use_container_width=True)
    except:
        st.info("Tips: Letakkan file 'sepeda.jpg' di folder dashboard untuk menampilkan logo.")

    st.title("🚲 Bike Sharing Filter")
    
    # Filter Rentang Waktu
    min_date = day_df["dteday"].min()
    max_date = day_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data utama berdasarkan tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# Menyiapkan data agregasi
season_df = create_season_rent_df(main_df)
weather_df = create_weather_rent_df(main_df)
weekday_df = create_weekday_rent_df(main_df)
rush_hour_df = create_rush_hour_df(hour_df) # Menggunakan data hour untuk rush hour
temp_df = create_temp_rent_df(main_df)

# ==============================
# MAIN LAYOUT
# ==============================
st.title("🚲 Bike Sharing Analytics Dashboard ✨")
st.markdown(f"Menampilkan data dari **{start_date}** hingga **{end_date}**")

# --- KINERJA UTAMA (METRICS) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Total Registered", value=f"{main_df['registered'].sum():,}")
with col3:
    st.metric("Total Casual", value=f"{main_df['casual'].sum():,}")

st.divider()

# --- VISUALISASI UTAMA ---
tab1, tab2, tab3, tab4 = st.tabs(["🌤️ Lingkungan", "🕒 Jam Sibuk", "👥 Profil Pengguna", "📝 Kesimpulan"])

with tab1:
    st.subheader("Analisis Faktor Lingkungan (Musim & Cuaca)")
    c1, c2 = st.columns(2)
    
    with c1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="season", y="cnt", data=season_df, palette="viridis", ax=ax)
        ax.set_title("Rata-rata Penyewaan per Musim", fontsize=15)
        ax.set_xlabel("Musim (1:Spring, 2:Summer, 3:Fall, 4:Winter)")
        st.pyplot(fig)
        
    with c2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="weathersit", y="cnt", data=weather_df, palette="coolwarm", ax=ax)
        ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca", fontsize=15)
        ax.set_xlabel("Cuaca (1:Cerah, 2:Mendung, 3:Hujan/Salju)")
        st.pyplot(fig)

    if temp_df is not None:
        st.write("#### Tren Berdasarkan Kategori Suhu (Binning Analysis)")
        fig, ax = plt.subplots(figsize=(15, 5))
        sns.barplot(x="temp_group", y="cnt", data=temp_df, palette="YlOrRd", ax=ax)
        st.pyplot(fig)

with tab2:
    st.subheader("Pola Penyewaan Jam Sibuk (Hari Kerja)")
    st.info("Data ini menggunakan dataset per jam untuk melihat pola komuter.")
    
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.lineplot(x="hr", y="cnt", data=rush_hour_df, marker='o', color='#2E86C1', linewidth=2.5, ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_title("Rata-rata Penyewaan per Jam pada Hari Kerja", fontsize=15)
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

with tab3:
    st.subheader("Perbandingan Pengguna: Casual vs Registered")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    weekday_melted = weekday_df.melt(id_vars='weekday', value_vars=['casual', 'registered'], 
                                     var_name='User Type', value_name='Average Rentals')
    
    sns.barplot(x='weekday', y='Average Rentals', hue='User Type', data=weekday_melted, palette='Set2', ax=ax)
    ax.set_title("Rata-rata Penyewaan Harian berdasarkan Tipe Pengguna", fontsize=15)
    ax.set_xlabel("Hari (0=Minggu, 6=Sabtu)")
    st.pyplot(fig)

with tab4:
    st.subheader("Kesimpulan & Rekomendasi Bisnis")
    st.markdown("""
    - **Musim & Cuaca:** Musim Gugur (Fall) dan Cuaca Cerah adalah pendorong utama penyewaan. Sebaliknya, cuaca buruk hampir menghentikan aktivitas penyewaan.
    - **Jam Sibuk:** Pada hari kerja, terjadi lonjakan tajam pada jam **08:00 pagi** dan **17:00-18:00 sore**, menunjukkan penggunaan sepeda untuk komuter kerja.
    - **Profil Pengguna:** Pengguna *Registered* stabil di hari kerja, sementara pengguna *Casual* meningkat drastis pada akhir pekan untuk rekreasi.
    
    **🚀 Rekomendasi:**
    1. Pastikan stok sepeda maksimal pada jam 07:00 dan 16:00 di area perkantoran.
    2. Berikan promo khusus pengguna Casual di hari Sabtu-Minggu untuk meningkatkan loyalitas.
    3. Lakukan maintenance armada pada Musim Semi (Spring) saat permintaan sedang rendah.
    """)

st.caption(f"Copyright © 2026 - Ning Ayu Lailatul Maghfiroh")
