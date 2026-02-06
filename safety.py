import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK BANNER TANGKI & UI MODERN ---
st.markdown("""
<style>
    /* Mengatur font agar lebih modern */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Banner Utama sesuai gambar yang diinginkan */
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 5rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-banner h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        margin: 0;
        font-weight: 700;
        color: #00f2ff; /* Cyan Neon */
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }

    .main-banner p {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        margin: 10px 0;
        font-weight: 400;
    }

    .tagline {
        background: #ffcc00;
        color: #000;
        padding: 5px 15px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
        display: inline-block;
        border-radius: 5px;
    }

    /* Styling Judul Dimensi Dinding */
    .dimensi-header {
        background-color: #ffffff;
        padding: 15px 25px;
        border-radius: 12px;
        margin: 2rem 0 1.5rem 0;
        border-left: 10px solid #1e3c72;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .dimensi-header h3 {
        margin: 0;
        color: #1e3c72;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <div style='display: flex; align-items: center; gap: 20px;'>
        <div style='font-size: 4rem;'></div>
        <div>
            <h1>BundSafe Tank Analytics</h1>
            <p>Bundwall & Storage Tank Safety Calculator</p>
            <div class='tagline'>Standardized by NFPA 30 | HSSE SULAWESI </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

st.markdown("---")

def number_input_zero(label, key):
    return st.number_input(label, min_value=0.0, value=0.0, key=key)

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    col1, col2, col3 = st.columns(3)
    panjang_luar = number_input_zero("Panjang Luar (m)", "p_luar")
    lebar_luar = number_input_zero("Lebar Luar (m)", "l_luar")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_dinding")
    
    # --- TAMBAHAN JUDUL DIMENSI ---
    st.markdown("### 🧱 Dimensi Dinding")
    
    col4, col5 = st.columns(2)
    lebar_atas = number_input_zero("Lebar Atas (m)", "lebar_atas")
    lebar_bawah = number_input_zero("Lebar Bawah (m)", "lebar_bawah")
    
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kapasitas")
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")

# Inisialisasi list untuk menyimpan 4 jenis data
d_pondasis_bawah = [0.0] * 5
d_pondasis_atas = [0.0] * 5
t_pondasis = [0.0] * 5
d_tanks = [0.0] * 5

for i in range(5):
    with st.expander(f"📍 Konfigurasi Tangki {i+1}"):
        # Membuat 4 kolom sejajar
        col1, col2, col3, col4 = st.columns(4)
        
        # Baris Inputan
        d_pondasis_bawah[i] = col1.number_input(f"D Pondasi Bawah {i+1} (m)", min_value=0.0, key=f"dp_bawah_{i}")
        d_pondasis_atas[i] = col2.number_input(f"D Pondasi Atas {i+1} (m)", min_value=0.0, key=f"dp_atas_{i}")
        t_pondasis[i] = col3.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, key=f"tp_{i}")
        d_tanks[i] = col4.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, key=f"dt_{i}")

# --- 3. INPUT SAFETY DISTANCE ---
st.markdown("---")
st.markdown("### 🛡️ Safety Distance")
st.info("Pilih tangki pembanding untuk menentukan jarak aman.")

col_sd1, col_sd2 = st.columns(2)

# Mengambil data otomatis dari input d_tanks di atas
pilih_t1 = col_sd1.selectbox("Tangki Pembanding 1:", options=range(5), 
                              format_func=lambda x: f"Tangki {x+1} (D={d_tanks[x]}m)")
pilih_t2 = col_sd2.selectbox("Tangki Pembanding 2:", options=range(5), 
                              format_func=lambda x: f"Tangki {x+1} (D={d_tanks[x]}m)")

d_safety_1 = d_tanks[pilih_t1]
d_safety_2 = d_tanks[pilih_t2]

col_prot, col_roof = st.columns(2)
proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_tr")
jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_tr")
    
    if st.button("💾 HITUNG", type="primary"):
        if panjang_luar == 0 or lebar_luar == 0 or tinggi_dinding == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            # --- RUMUS EXCEL PERSIS (Penerjemahan Langsung) ---
            # Term 1: ((( (C5-(2*C10)) + (C5-((C9+((C10-C9)/2))*2)) ) / 2 * C7) * (C6-(2*C10)))
            t1_a = (panjang_luar - (2 * lebar_bawah))
            t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
            term1 = ((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))

            # Term 2: (( (C10*((C10-C9)/2))/2 ) * (C5-(((C10-C9)/2)+C10)) * 2)
            s_val = (lebar_bawah - lebar_atas) / 2
            term2 = ((lebar_bawah * s_val) / 2) * (panjang_luar - (s_val + lebar_bawah)) * 2

            vol_bruto = term1 + term2
            # Vol Pond+Tank 10 terms EXCEL
            vol_pond_tank = 0
            for i in range(5):
                vol_pond_tank += (math.pi * ((d_pondasis[i]/2)**2) * t_pondasis[i]) + \
                                 (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
            
            vol_efektif_bund = vol_bruto - vol_pond_tank

            if vol_pond_tank > vol_efektif_bund:
                status = "✗ NON COMPLY - Volume bund kurang"
            if tinggi_dinding > 1.8:
                status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
            else:
                status = "✓ COMPLY - AMAN" if vol_efektif_bund > kapasitas_tank_besar * 1.1 else "✗ NON COMPLY"
            
        # --- B. Kalkulasi Safety Distance (Revisi Sesuai Logika Excel & Input d_safety) ---
            
            # max_d_s untuk menentukan pembagi shell to shell
            max_d_s = max(d_safety_1, d_safety_2)
            
            # 1. Shell to Shell (1/6 jika <= 45m, 1/3 jika > 45m)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            
            # 2. Tank to Building (Sesuai Rumus: ROUND(MAX(1.5; IF...)))
            if jenis_tank == "Floating Roof":
                f_build = 1/6
            elif proteksi == "Proteksi":
                f_build = 1/6
            else:
                f_build = 1/3
            
            # Menggunakan d_safety_1 sebagai C15 (Diameter Tangki Utama)
            tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
            
            # 3. Tank to Property (Sesuai Rumus: ROUND(MAX(1.5; IF...)))
            if jenis_tank == "Floating Roof":
                if proteksi == "Proteksi":
                    f_prop = 1/2
                else:
                    f_prop = 1
            else:
                if proteksi == "Proteksi":
                    f_prop = 1/2
                else:
                    f_prop = 2
                    
            tank_to_property = round(max(1.5, f_prop * d_safety_1), 2)
            st.markdown("### 📈 HASIL PERHITUNGAN")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col_res2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Status Safety", status)
        with col_res3:
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
                st.metric("Tank to Building (m)", f"{tank_to_build:.2f}")
                st.metric("Tank to Property (m)", f"{tank_to_property:.2f}")
       
else:  # Persegi
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    panjang = number_input_zero("Panjang (m)", "p_per")
    lebar = number_input_zero("Lebar (m)", "l_per")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_per")
    
     # --- TAMBAHAN JUDUL DIMENSI ---
    st.markdown("### 🧱 Dimensi Dinding")
    
    col4, col5 = st.columns(2)
    lebar_dinding = number_input_zero("Lebar Dinding  (m)", "ld1_per")
    Panjang_dinding = number_input_zero("Panjang Dinding  (m)", "ld2_per")
    
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kap_per")
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    d_pondasis = [0]*5
    t_pondasis = [0]*5
    d_tanks = [0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            d_pondasis[i] = number_input_zero(f"Diameter Pondasi {i+1} (m)", f"dpond_per_{i}")
            t_pondasis[i] = number_input_zero(f"Tinggi Pondasi {i+1} (m)", f"tpond_per_{i}")
            d_tanks[i] = number_input_zero(f"Diameter Tangki {i+1} (m)", f"dtank_per_{i}")
            
     # 2. TAMBAHAN INPUT SAFETY DISTANCE (SESUDAH TANGKI+PONDASI)
    st.markdown("### 🛡️ Safety Distance ")
    st.info("Gunakan diameter di bawah ini khusus untuk menentukan jarak aman antar tangki.")
    col_sd1, col_sd2 = st.columns(2)
    d_safety_1 = col_sd1.number_input("Diameter Tangki Pembanding 1 (m)", min_value=0.0, key="sd_d1")
    d_safety_2 = col_sd2.number_input("Diameter Tangki Pembanding 2 (m)", min_value=0.0, key="sd_d2")
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_per")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_per")
    
    if st.button("💾 HITUNG", type="primary"):
        if panjang == 0 or lebar == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*Panjang_dinding)
            
            vol_pond_tank = 0
            for i in range(5):
                vol_pond_tank += (math.pi * ((d_pondasis[i]/2)**2) * t_pondasis[i]) + \
                                 (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            
            if vol_pond_tank > vol_efektif_bund:
                status = "✗ NON COMPLY - Volume bund kurang"
            elif tinggi_dinding > 1.8:
                status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
            else:
                status = "✓ COMPLY - AMAN" if kapasitas_tank_besar * 1.1 <= vol_efektif_bund else "CHECK DATA"
            
             # Kalkulasi Safety Distance (Berdasarkan Input Baru)
            max_d_s = max(d_safety_1, d_safety_2)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            
            f_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
            tank_to_build = max(1.5, f_build * d_safety_1)
            
            st.markdown("### 📈 HASIL PERHITUNGAN")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col_res2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Status Safety", status)
            with col3:
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
                st.metric("Tank to Building (m)", tank_to_building)
                st.metric("Tank to Property (m)", tank_to_property)
