# Air Quality Data Analysis Project (Beijing)
## Submission: Proyek Analisis Data - Kualitas Udara Dataset

### 📋 Informasi Pengumpul
- **Nama:** Innayatul Laili Husnaini
- **Email:** cdcc283d6x2283@student.devacademy.id
- **ID Dicoding:** CDCC283D6X2283
- **Data:** PRSA Data (Beijing Air Pollution Monitoring 2013-2017)
- **Total Records:** 420,768
- **Lokasi Pemantauan:** 12 titik di Beijing

---

## 📊 Struktur Submission

### 1. **Notebook Analisis** (`Proyek_Analisis_Data.ipynb`)
Notebook lengkap yang memenuhi seluruh kriteria submission:

#### ✅ Kriteria 1: Menentukan Pertanyaan Bisnis (SMART Questions)

**Pertanyaan 1:** 
> "Bagaimana pola perubahan konsentrasi PM2.5 per jam dalam sehari di lokasi Dongsi Beijing selama periode 2013-2017, dan jam-jam mana saja yang memiliki tingkat polusi tertinggi sehingga memerlukan intervensi khusus?"

- **Specific**: Focus pada PM2.5 per jam di lokasi Dongsi
- **Measurable**: Konsentrasi dalam µg/m³ per jam
- **Action-Oriented**: Identifikasi jam puncak untuk program kontrol lalu lintas
- **Relevant**: Untuk kebijakan kontrol kualitas udara  
- **Time-bound**: Periode 2013-2017

**Pertanyaan 2:**
> "Apakah terdapat perbedaan signifikan dalam tingkat polutan PM2.5 antara 12 lokasi pemantauan di Beijing, dan lokasi mana yang konsisten memiliki kualitas udara terburuk selama periode 2015-2017 untuk menjadi fokus program perbaikan lingkungan?"

- **Specific**: Perbandingan PM2.5 antar 12 lokasi
- **Measurable**: Rata-rata konsentrasi PM2.5 per lokasi
- **Action-Oriented**: Alokasi intervensi ke lokasi prioritas
- **Relevant**: Untuk strategi perbaikan kualitas udara yang targeted
- **Time-bound**: Periode 2015-2017

---

#### ✅ Kriteria 2: Data Wrangling

**Gathering Data:**
- Membaca 12 file CSV dari berbagai stasiun pemantauan
- Menggabungkan semua data menjadi satu DataFrame
- Total 420,768 records dengan 19 kolom

**Assessing Data (Masalah yang Ditemukan):**
1. **Missing Values**: Ditemukan pada kolom meteorologi (TEMP, PRES, DEWP, RAIN, WSPM)
2. **Invalid Datetime**: Beberapa kombinasi tahun-bulan-hari tidak valid
3. **Data Type Inconsistency**: Kolom numerik berisi NaN yang perlu konversi

**Cleaning Data:**
- Mengisi missing values dengan forward fill dan mean per stasiun
- Validasi dan konversi datetime
- Menghapus rows dengan datetime invalid
- Sort data chronologically

**Output**: Clean dataset siap untuk analisis dengan 420,768 records

---

#### ✅ Kriteria 3: Exploratory Data Analysis (EDA)

**Explorasi untuk Pertanyaan 1 (Pola Jam-jam Puncak):**
- Analisis statistik PM2.5 per jam di Dongsi
- Hasil: PM2.5 tertinggi pada jam 22:00 (97.66 µg/m³)
- Hasil: PM2.5 terendah pada jam 15:00 (78.21 µg/m³)
- Perbedaan: 19.45 µg/m³ (24.8% dari rata-rata)
- Analisis tren bulanan menunjukkan polusi lebih tinggi di musim dingin (Desember-Januari)

**Explorasi untuk Pertanyaan 2 (Perbandingan Lokasi):**
- Analisis PM2.5 per lokasi (2015-2017)
- Lokasi Terburuk: Dongsi (85.20 µg/m³)
- Lokasi Terbaik: Dingling (64.11 µg/m³)
- Perbedaan: 21.09 µg/m³ (33% perbedaan)
- Trend tahunan: Perbaikan 2015→2016, kemudian memburuk 2016→2017

---

#### ✅ Kriteria 4: Visualization & Explanatory Analysis

**Visualisasi Pertanyaan 1:**
1. Line plot dengan confidence interval: Pola harian PM2.5 di Dongsi
2. Bar chart: Identifikasi jam puncak (merah) dan lembah (biru)
- Insight: Pola bimodal dengan puncak di malam/pagi (peak traffic hours)

**Visualisasi Pertanyaan 2:**
1. Horizontal bar chart: Perbandingan rata-rata PM2.5 antar lokasi
2. Box plot: Distribusi dan variasi per lokasi
3. Line plot: Trend tahunan untuk 3 lokasi terburuk
- Insight: Lokasi urban center (Dongsi, Wanshouxigong) konsisten terburuk

---

#### ✅ Kriteria 5: Conclusion & Recommendation

**Kesimpulan:**
1. **Kesimpulan Pertanyaan 1:** 
   - Pola PM2.5 di Dongsi menunjukkan fluktuasi harian yang signifikan
   - Jam puncak: 22:00-01:00 (malam) dan 07:00-09:00 (pagi)
   - Menunjukkan pengaruh aktivitas manusia (traffic, pemanas ruangan)

2. **Kesimpulan Pertanyaan 2:**
   - Disparitas kualitas udara antar lokasi mencapai 21 µg/m³
   - Lokasi urban center (Dongsi, Wanshouxigong) prioritas intervensi
   - Trend positif 2015-2016, namun reversing di 2017

**Rekomendasi Action Item:**
1. **Traffic Management Program**: Even-odd license plate system pada jam puncak (-15-20% emisi)
2. **Real-time Monitoring & Early Warning**: Alert system untuk publik di area high-pollution
3. **Public Health Campaign**: Edukasi risiko PM2.5 dan penggunaan masker N95
4. **Green Transportation Investment**: Ekspansi public transport untuk menggantikan 30% kendaraan pribadi
5. **Industrial Emission Standards**: Regulasi ketat pada pabrik di area terburuk

---

### 2. **Dashboard Interaktif** (`dashboard_air_quality.py`)

Streamlit dashboard dengan fitur interaktif untuk visualisasi hasil analisis:

**Fitur Dashboard:**
- ✅ Filter by date range
- ✅ Multi-select station
- ✅ Pollutant selection (PM2.5, PM10, SO2, NO2, CO, O3)
- ✅ KPI cards (Avg, Max, Min, Unhealthy Days)
- ✅ 4 Tab sections:
  - **Tab 1:** Pola jam-jam puncak (Pertanyaan 1)
  - **Tab 2:** Perbandingan antar lokasi (Pertanyaan 2)
  - **Tab 3:** Analisis temporal (trend bulanan & tahunan)
  - **Tab 4:** Data explorer dengan download CSV

**Cara Menjalankan Dashboard:**
```bash
cd "d:\DBS 2026\PROYEK FUNDAMENTAL ANALISIS DATA"
streamlit run dashboard_air_quality.py
```

Dashboard akan membuka di browser `http://localhost:8501`

---

### 3. **Struktur File**

```
PROYEK FUNDAMENTAL ANALISIS DATA/
├── Proyek_Analisis_Data.ipynb          # Main analysis notebook
├── dashboard_air_quality.py             # Streamlit dashboard
├── README.md                            # This file
├── Air-quality-dataset.zip              # Original dataset
└── Air-quality-dataset/
    └── PRSA_Data_20130301-20170228/
        ├── PRSA_Data_Aotizhongxin_*.csv
        ├── PRSA_Data_Changping_*.csv
        ├── PRSA_Data_Dingling_*.csv
        ├── PRSA_Data_Dongsi_*.csv
        ├── PRSA_Data_Guanyuan_*.csv
        ├── PRSA_Data_Gucheng_*.csv
        ├── PRSA_Data_Huairou_*.csv
        ├── PRSA_Data_Nongzhanguan_*.csv
        ├── PRSA_Data_Shunyi_*.csv
        ├── PRSA_Data_Tiantan_*.csv
        ├── PRSA_Data_Wanliu_*.csv
        └── PRSA_Data_Wanshouxigong_*.csv
```

---

## 📦 Dependency & Requirements

**Python Libraries Required:**
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn (untuk clustering & PCA)
- streamlit

**Install via:**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit
```

**Python Version:** 3.8+

---

## 🎯 Checklist Completion

- ✅ **Kriteria 1**: 2 SMART Questions with proper framework
- ✅ **Kriteria 2**: Data Wrangling (Gathering → Assessing → Cleaning) dengan minimum 2 masalah teridentifikasi
- ✅ **Kriteria 3**: EDA untuk menjawab kedua pertanyaan bisnis
- ✅ **Kriteria 4**: Minimum 2 visualisasi yang rapi dan informatif
- ✅ **Kriteria 5**: 2 kesimpulan + minimal 1 rekomendasi action item
- ✅ **Kriteria 6**: Notebook yang rapi sesuai template
- ✅ **Kriteria 7**: Dashboard Streamlit yang berjalan lancar

---

## 📈 Key Findings Summary

### Question 1 Results:
- **Peak Pollution Hours**: 22:00-01:00 (97.7 µg/m³) & 06:00-09:00
- **Lowest Pollution Hours**: 15:00-17:00 (78.2 µg/m³)
- **Peak-to-Low Difference**: 19.5 µg/m³ (24.8%)

### Question 2 Results:
- **Worst Location**: Dongsi (85.2 µg/m³)
- **Best Location**: Dingling (64.1 µg/m³)
- **Location Disparity**: 21.1 µg/m³ (33%)
- **Worst 3 Locations**: Dongsi, Wanshouxigong, Nongzhanguan

### Advanced Analysis Results (Optional Section):

**1. Pollutant Correlation:**
- PM2.5 ↔ PM10: 0.876 (Very Strong)
- PM2.5 ↔ CO: 0.773 (Strong) → Vehicle emissions primary source
- NO2 ↔ O3: -0.455 (Inverse) → Atmospheric chemistry effect

**2. Seasonal Pattern:**
- Early Winter: **104.3 µg/m³** (Peak - heating system effect)
- Summer: **64.8 µg/m³** (Best - better atmospheric dispersion)
- Difference: **60% higher** in early winter vs summer

**3. Spatial Clustering:**
- **Urban Core** (8 locations): 84.2 µg/m³ - Downtown/CBD
- **Suburban** (2 locations): 75.6 µg/m³ - Developing areas
- **Rural** (2 locations): 68.7 µg/m³ - Periphery

**4. Long-term Trends:**
- 2013→2014: Deterioration (86.7 µg/m³)
- 2014→2016: Improvement (72.4 µg/m³ - Best year)
- 2016→2017: Backsliding (92.6 µg/m³)
- Pattern suggests policy effectiveness decreased over time

**5. Extreme Events:**
- Only **13.6%** of time with "Good" air quality
- **35% of time** in "Unhealthy" category
- **4.6% hazardous events** (PM2.5 > 150)
- Extreme peak: **999 µg/m³** on Feb 8, 2016

---

## 📞 Contact & Support

Untuk pertanyaan atau bantuan terkait submission ini:
- Email: cdcc283d6x2283@student.devacademy.id
- ID Dicoding: CDCC283D6X2283

---

**Last Updated**: April 28, 2026
**Status**: ✅ Ready for Submission
