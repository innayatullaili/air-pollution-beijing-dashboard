import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Kualitas Udara",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set gaya visualisasi
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

# Muat data
@st.cache_data
def load_data():
    """Muat dan proses data kualitas udara"""
    # Coba muat dari main_data.csv terlebih dahulu
    main_data_path = Path(__file__).parent.parent / 'data' / 'main_data.csv'
    
    if main_data_path.exists():
        df = pd.read_csv(main_data_path)
    else:
        # Fallback: muat dari individual CSV files
        data_folder = Path(__file__).parent.parent / 'data'
        csv_files = list(data_folder.glob('PRSA_Data_*.csv'))
        
        if not csv_files:
            st.error("❌ Data files tidak ditemukan! Pastikan folder 'data' berisi CSV files.")
            st.stop()
        
        dfs = []
        for file in sorted(csv_files):
            station_name = file.stem.split('_')[2]  # Ekstrak nama stasiun
            df_temp = pd.read_csv(file)
            df_temp['Station'] = station_name
            dfs.append(df_temp)
        
        df = pd.concat(dfs, ignore_index=True)
    
    df = pd.concat(dfs, ignore_index=True)
    
    # Bersihkan nama kolom - pertahankan 'Station' untuk sekarang
    cols_lower = {col: col.lower() for col in df.columns if col != 'Station'}
    df = df.rename(columns=cols_lower)
    
    # Hapus kolom 'no' jika ada
    if 'no' in df.columns:
        df = df.drop('no', axis=1)
    
    # Buat kolom datetime
    df['datetime'] = pd.to_datetime(
        df[['year', 'month', 'day', 'hour']],
        errors='coerce'
    )
    
    # Tangani nilai yang hilang
    numeric_cols = ['pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Isi nilai yang hilang dengan rata-rata per stasiun
            df[col] = df.groupby('Station')[col].transform(
                lambda x: x.ffill().fillna(x.mean())
            )
    
    # Hapus baris dengan datetime yang tidak valid
    df = df.dropna(subset=['datetime'])
    df = df.sort_values('datetime').reset_index(drop=True)
    
    print(f"✅ Data berhasil dimuat!")
    print(f"Total baris: {len(df)}")
    print(f"Stasiun ditemukan: {df['Station'].unique().tolist()}")
    
    return df

# Muat data
df = load_data()

# Tambah kolom turunan
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day
df['hour'] = df['datetime'].dt.hour
df['month_name'] = df['datetime'].dt.strftime('%B')

# Custom CSS
st.markdown("""
    <style>
    .header-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Bilah sisi
with st.sidebar:
    st.title("🔧 Filter & Kontrol")
    st.markdown("---")
    
    # Pilih rentang tanggal
    min_date = df['datetime'].min().date()
    max_date = df['datetime'].max().date()
    
    date_range = st.date_input(
        "Pilih Periode Waktu",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Pilih stasiun
    stations = sorted(df['Station'].unique())
    # Atur stasiun default hanya jika ada di data
    default_stations = [s for s in ['Dongsi', 'Chaoyang', 'Guanyuan'] if s in stations]
    if not default_stations:  # Fallback jika tidak ada
        default_stations = stations[:3] if len(stations) >= 3 else stations
    
    selected_stations = st.multiselect(
        "Pilih Lokasi Pemantauan",
        options=stations,
        default=default_stations
    )
    
    # Pilih polutan
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    selected_pollutant = st.selectbox(
        "Pilih Polutan untuk Analisis",
        options=pollutants,
        index=0
    )
    
    st.markdown("---")
    st.info("Dashboard ini menganalisis data kualitas udara Beijing dari 12 lokasi pemantauan selama 2013-2017.")

# Filter data berdasarkan pilihan
if len(date_range) == 2:
    df_filtered = df[
        (df['datetime'].dt.date >= date_range[0]) & 
        (df['datetime'].dt.date <= date_range[1]) &
        (df['Station'].isin(selected_stations))
    ]
else:
    df_filtered = df[df['Station'].isin(selected_stations)]

# Judul utama
st.markdown('<div class="header-title">🌍 Dashboard Analisis Kualitas Udara</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pemantauan Polusi Udara Beijing (2013-2017)</div>', 
            unsafe_allow_html=True)

# Bagian KPI
st.markdown("## 📊 Indikator Kinerja Utama")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_pm25 = df_filtered['pm2.5'].mean()
    st.metric(
        label="Rata-rata PM2.5",
        value=f"{avg_pm25:.1f} µg/m³",
        delta=f"{avg_pm25 - 35:.1f} µg/m³" if avg_pm25 > 35 else "Normal",
        delta_color="inverse"
    )

with col2:
    max_pm25 = df_filtered['pm2.5'].max()
    st.metric(
        label="Maks PM2.5",
        value=f"{max_pm25:.1f} µg/m³"
    )

with col3:
    min_pm25 = df_filtered['pm2.5'].min()
    st.metric(
        label="Min PM2.5",
        value=f"{min_pm25:.1f} µg/m³"
    )

with col4:
    days_unhealthy = len(df_filtered[df_filtered['pm2.5'] > 75])
    total_days = len(df_filtered['datetime'].dt.date.unique()) if len(df_filtered) > 0 else 0
    st.metric(
        label="Hari Tidak Sehat",
        value=f"{days_unhealthy}",
        delta=f"dari {total_days} hari" if total_days > 0 else "N/A"
    )

st.markdown("---")

# Tab sections
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Pertanyaan 1: Pola Jam-jam Puncak",
    "🗺️ Pertanyaan 2: Perbandingan Antar Lokasi",
    "📊 Analisis Temporal",
    "🔍 Data Explorer"
])

# TAB 1: Pola Jam-jam Puncak (Pertanyaan 1)
with tab1:
    st.header("Pola Konsentrasi PM2.5 Per Jam di Lokasi Terpilih")
    st.markdown("""
    **Pertanyaan:** Bagaimana pola perubahan konsentrasi PM2.5 per jam dalam sehari, 
    dan jam-jam mana saja yang memiliki tingkat polusi tertinggi?
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pilih stasiun spesifik untuk analisis per jam detail
        detailed_station = st.selectbox(
            "Pilih Lokasi untuk Analisis Jam-jam Puncak",
            options=selected_stations,
            key="hourly_station"
        )
        
        station_data = df_filtered[df_filtered['Station'] == detailed_station].copy()
        hourly_avg = station_data.groupby('hour')['pm2.5'].agg(['mean', 'std', 'count'])
        
        # Buat gambar
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot
        ax.plot(hourly_avg.index, hourly_avg['mean'], 
                marker='o', linewidth=2.5, markersize=8, color='#d62728', label='Rata-rata PM2.5')
        ax.fill_between(hourly_avg.index, 
                        hourly_avg['mean'] - hourly_avg['std'],
                        hourly_avg['mean'] + hourly_avg['std'],
                        alpha=0.2, color='#d62728')
        
        # Pemformatan
        ax.set_xlabel('Jam dalam Sehari (Hour)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Konsentrasi PM2.5 (µg/m³)', fontsize=11, fontweight='bold')
        ax.set_title(f'Pola Harian PM2.5 di {detailed_station}', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(0, 24, 2))
        ax.axhline(y=35, color='orange', linestyle='--', linewidth=2, label='Panduan WHO (35 µg/m³)')
        ax.legend(loc='best')
        
        st.pyplot(fig)
    
    with col1:
        # Temukan jam puncak
        peak_hour = hourly_avg['mean'].idxmax()
        low_hour = hourly_avg['mean'].idxmin()
        
        st.success(f"**Jam Puncak Polusi:** {peak_hour}:00 (Rata-rata: {hourly_avg.loc[peak_hour, 'mean']:.1f} µg/m³)")
        st.info(f"**Jam Lembah Polusi:** {low_hour}:00 (Rata-rata: {hourly_avg.loc[low_hour, 'mean']:.1f} µg/m³)")
    
    with col2:
        st.subheader("Statistik per Jam")
        st.dataframe(hourly_avg.round(2))

# TAB 2: Perbandingan Antar Lokasi (Pertanyaan 2)
with tab2:
    st.header("Perbandingan Kualitas Udara Antar Lokasi Pemantauan")
    st.markdown("""
    **Pertanyaan:** Apakah terdapat perbedaan signifikan PM2.5 antar 12 lokasi, 
    dan lokasi mana yang memiliki kualitas udara terburuk?
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bagan perbandingan
        station_stats = df_filtered.groupby('Station')['pm2.5'].agg(['mean', 'median', 'std', 'min', 'max']).sort_values('mean', ascending=False)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        colors = ['#d62728' if i < 3 else '#ff7f0e' if i < 6 else '#1f77b4' 
                 for i in range(len(station_stats))]
        bars = ax.barh(station_stats.index, station_stats['mean'], color=colors, edgecolor='black', alpha=0.8)
        
        # Tambahkan nilai pada batang
        for i, v in enumerate(station_stats['mean'].values):
            ax.text(v + 1, i, f'{v:.1f}', va='center', fontweight='bold')
        
        ax.axvline(x=35, color='orange', linestyle='--', linewidth=2, label='Panduan WHO')
        ax.set_xlabel('Rata-rata PM2.5 (µg/m³)', fontsize=11, fontweight='bold')
        ax.set_title('Perbandingan Rata-rata PM2.5 Antar Lokasi', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        ax.legend()
        
        st.pyplot(fig)
    
    with col2:
        st.subheader("Ranking Lokasi")
        for idx, (station, row) in enumerate(station_stats.iterrows(), 1):
            emoji = "🔴" if idx <= 3 else "🟠" if idx <= 6 else "🟢"
            st.write(f"{emoji} **#{idx}** {station}: {row['mean']:.1f} µg/m³")

# TAB 3: Analisis Temporal
with tab3:
    st.header("Analisis Temporal: Tren Waktu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tren Bulanan")
        monthly_avg = df_filtered.groupby('month')['pm2.5'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly_avg.index, monthly_avg.values, marker='o', linewidth=2.5, markersize=8, color='#1f77b4')
        ax.fill_between(monthly_avg.index, monthly_avg.values, alpha=0.3, color='#1f77b4')
        ax.set_xlabel('Bulan', fontsize=10, fontweight='bold')
        ax.set_ylabel('PM2.5 (µg/m³)', fontsize=10, fontweight='bold')
        ax.set_title('Pola Bulanan PM2.5', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(1, 13))
        ax.axhline(y=35, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Tren Tahunan")
        yearly_avg = df_filtered.groupby('year')['pm2.5'].mean()
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(yearly_avg.index, yearly_avg.values, marker='s', linewidth=2.5, markersize=10, color='#2ca02c')
        ax.fill_between(yearly_avg.index, yearly_avg.values, alpha=0.3, color='#2ca02c')
        ax.set_xlabel('Tahun', fontsize=10, fontweight='bold')
        ax.set_ylabel('PM2.5 (µg/m³)', fontsize=10, fontweight='bold')
        ax.set_title('Pola Tahunan PM2.5', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_xticks(df_filtered['year'].unique())
        ax.axhline(y=35, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
        st.pyplot(fig)

# TAB 4: Data Explorer
with tab4:
    st.header("🔍 Data Explorer")
    
    # Statistics by station
    st.subheader("Statistik Deskriptif per Lokasi")
    stat_table = df_filtered.groupby('Station')['pm2.5'].describe().round(2)
    st.dataframe(stat_table)
    
    # Raw data viewer
    st.subheader("Data Lengkap")
    display_cols = ['datetime', 'Station', 'pm2.5', 'pm10', 'so2', 'no2', 'co', 'o3']
    available_cols = [col for col in display_cols if col in df_filtered.columns]
    
    if st.checkbox("Tampilkan Raw Data"):
        st.dataframe(df_filtered[available_cols].tail(100), use_container_width=True)
    
    # Download data
    csv = df_filtered[available_cols].to_csv(index=False)
    st.download_button(
        label="📥 Download Data sebagai CSV",
        data=csv,
        file_name=f"air_quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p><strong>Dashboard Analisis Data Kualitas Udara Beijing</strong></p>
    <p>Nama: Innayatul Laili Husnaini | Email: cdcc283d6x2283@student.devacademy.id | ID: CDCC283D6X2283</p>
    <p>Data: PRSA Data (2013-2017) | Dashboard: Streamlit</p>
</div>
""", unsafe_allow_html=True)
