import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur layout halaman Streamlit agar lebih lebar (wide)
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Mengatur tema seaborn
sns.set_theme(style="whitegrid")

# ==============================
# HELPER FUNCTIONS (Fungsi Bantuan)
# ==============================
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return daily_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by="season")[["cnt"]].mean().reset_index()
    return season_rent_df

def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by="weathersit")[["cnt"]].mean().reset_index()
    return weather_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by="weekday")[["casual", "registered"]].mean().reset_index()
    # Menyesuaikan urutan hari
    days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekday_rent_df['weekday'] = pd.Categorical(weekday_rent_df['weekday'], categories=days_order, ordered=True)
    weekday_rent_df = weekday_rent_df.sort_values('weekday')
    return weekday_rent_df

def create_temp_rent_df(df):
    temp_rent_df = df.groupby(by="temp_group")[["cnt"]].mean().reset_index()
    return temp_rent_df

# ==============================
# LOAD DATA
# ==============================
# Membaca data yang sudah dibersihkan
all_df = pd.read_csv("submission_dicoding/dashboard/main_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# ==============================
# SIDEBAR (Bagian Kiri)
# ==============================
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Memasukkan gambar lokal (Pastikan nama filenya sepeda.png dan ada di folder yang sama)
    st.image("submission_dicoding/dashboard/sepeda.png", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>🚲 Bike Rent Filter</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filter rentang waktu
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu:',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    st.markdown("---")
    st.caption("Proyek Analisis Data © 2024")

# ==============================
# FILTER DATA UTAMA
# ==============================
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                 (all_df["dteday"] <= str(end_date))]

# Menyiapkan dataframe untuk visualisasi
daily_rent_df = create_daily_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
temp_rent_df = create_temp_rent_df(main_df)

# ==============================
# MAIN DASHBOARD (Bagian Kanan)
# ==============================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard ini menampilkan performa penyewaan sepeda berdasarkan berbagai faktor seperti musim, cuaca, dan profil pengguna.")

# --- 1. METRICS (Angka Kinerja) ---
st.subheader("📊 Ringkasan Data (Rentang Waktu Terpilih)")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewaan", value=f"{daily_rent_df['cnt'].sum():,}")
with col2:
    st.metric("Penyewa Terdaftar (Registered)", value=f"{daily_rent_df['registered'].sum():,}")
with col3:
    st.metric("Penyewa Biasa (Casual)", value=f"{daily_rent_df['casual'].sum():,}")

st.markdown("---")

# --- 2. TABS UNTUK VISUALISASI ---
# Menggunakan Tabs agar dashboard terlihat rapi dan tidak terlalu panjang ke bawah
tab1, tab2, tab3 = st.tabs(["📈 Tren Harian", "⛅ Musim & Cuaca", "👥 Profil Pengguna"])

# TAB 1: TREN HARIAN
with tab1:
    st.subheader("Tren Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(16, 6))
    sns.lineplot(x="dteday", y="cnt", data=daily_rent_df, marker="o", color="#2E86C1", linewidth=2.5, ax=ax)
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xlabel("Tanggal")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# TAB 2: MUSIM & CUACA
with tab2:
    st.subheader("Dampak Faktor Lingkungan terhadap Penyewaan")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x="season", y="cnt", data=season_rent_df, palette="viridis", ax=ax)
        ax.set_title("Rata-rata Penyewaan per Musim")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)
        
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x="weathersit", y="cnt", data=weather_rent_df, palette="magma", ax=ax)
        ax.set_title("Rata-rata Penyewaan per Kondisi Cuaca")
        ax.set_xlabel("Cuaca")
        ax.set_ylabel("")
        st.pyplot(fig)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("💡 **Insight:** Suhu dan cuaca sangat memengaruhi jumlah penyewaan. Rentang suhu *Sedang* hingga *Panas* sangat diminati, sementara cuaca *Buruk (Heavy Rain/Snow)* hampir menghentikan penyewaan.")
    
    # Analisis Lanjutan: Suhu
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x="temp_group", y="cnt", data=temp_rent_df, palette="coolwarm", ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kategori Suhu")
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

# TAB 3: PROFIL PENGGUNA
with tab3:
    st.subheader("Perbandingan Tipe Pengguna: Casual vs Registered")
    st.markdown("Grafik ini menunjukkan perbedaan perilaku antara pelanggan biasa (Casual) dan pelanggan langganan (Registered) pada hari kerja dan akhir pekan.")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    weekday_melted = weekday_rent_df.melt(id_vars='weekday', value_vars=['casual', 'registered'], 
                                         var_name='User Type', value_name='Average Rentals')
    
    sns.barplot(x='weekday', y='Average Rentals', hue='User Type', data=weekday_melted, palette='Set2', ax=ax)
    ax.set_title("Rata-rata Penyewaan Harian berdasarkan Tipe Pengguna")
    ax.set_xlabel("Hari dalam Seminggu")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
