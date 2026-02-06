import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK UI MODERN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
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
        color: #00f2ff;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }

    .main-banner p {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        margin: 10px 0;
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
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div class='tagline'>Standardized by NFPA 30 | HSSE SULAWESI </div>
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

# Inisialisasi list penampung data tangki
d_atas_pond = [0.0] * 5
d_bawah_pond = [0.0] * 5
t_pondasis = [0.0] * 5
d_tanks = [0.0] * 5

# --- KONDISI 1: TRAPESIUM ---
if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar_tr")
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar_tr")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding_tr")
    
    st.markdown("### 🧱 Dimensi Dinding")
    col4, col5, col6 = st.columns(3)
    lebar_atas = col4.number_input("Lebar Atas Dinding (m)", min_value=0.0, key="lebar_atas_tr")
    lebar_bawah = col5.number_input("Lebar Bawah Dinding (m)", min_value=0.0, key="lebar_bawah_tr")
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kap_tr")
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    for i in range(5):
        with st.expander(f"📍 Konfigurasi Tangki {i+1}"):
            c1, c2, c3, c4 = st.columns(4)
            d_atas_pond[i] = c1.number_input(f"D. Atas Pond {i+1} (m)", min_value=0.0, key=f"da_tr_{i}")
            d_bawah_pond[i] = c2.number_input(f"D. Bawah Pond {i+1} (m)", min_value=0.0, key=f"db_tr_{i}")
            t_pondasis[i] = c3.number_input(f"Tinggi Pond {i+1} (m)", min_value=0.0, key=f"tp_tr_{i}")
            d_tanks[i] = c4.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, key=f"dt_tr_{i}")

    st.markdown("### 🛡️ Safety Distance")
    col_sd1, col_sd2 = st.columns(2)
    d_safety_1 = col_sd1.number_input("Diameter Tangki Pembanding 1 (m)", min_value=0.0, key="sd_d1_tr")
    d_safety_2 = col_sd2.number_input("Diameter Tangki Pembanding 2 (m)", min_value=0.0, key="sd_d2_tr")
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_tr")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_tr")

    if st.button("💾 HITUNG", type="primary", key="btn_tr"):
        if panjang_luar == 0 or lebar_luar == 0 or tinggi_dinding == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            # Perhitungan Bruto Trapesium (Kurung diperbaiki agar tidak SyntaxError)
            t1_a = (panjang_luar - (2 * lebar_bawah))
            t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
            term1 = ((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))

            s_val = (lebar_bawah - lebar_atas) / 2
            term2 = ((lebar_bawah * s_val) / 2) * (panjang_luar - (s_val + lebar_bawah)) * 2
            vol_bruto = term1 + term2

            # Volume Pengurang (Pondasi & Tangki)
            vol_pond_tank = 0
            for i in range(5):
                vol_pond_tank += (math.pi * ((d_bawah_pond[i]/2)**2) * t_pondasis[i]) + \
                                 (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            status = "✓ COMPLY" if vol_efektif_bund > (kapasitas_tank_besar * 1.1) and tinggi_dinding <= 1.8 else "✗ NON COMPLY"

            # Safety Distance Calc
            max_d_s = max(d_safety_1, d_safety_2)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
            tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
            tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else 2.0) * d_safety_1), 2)

            st.markdown("### 📈 HASIL PERHITUNGAN")
            res1, res2, res3 = st.columns(3)
            res1.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
            res1.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            res2.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
            res2.metric("Status Safety", status)
            res3.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            res3.metric("Tank to Building (m)", f"{tank_to_build}")
            res3.metric("Tank to Property (m)", f"{tank_to_property}")

# --- KONDISI 2: PERSEGI ---
else:
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0, key="p_per")
    lebar = col2.number_input("Lebar (m)", min_value=0.0, key="l_per")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_per")
    
    st.markdown("### 🧱 Dimensi Dinding")
    col4, col5, col6 = st.columns(3)
    lebar_dinding = col4.number_input("Lebar Dinding (m)", min_value=0.0, key="ld1_per")
    panjang_tebal = col5.number_input("Ketebalan Dinding (m)", min_value=0.0, key="ld2_per")
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kap_per")
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    for i in range(5):
        with st.expander(f"📍 Konfigurasi Tangki {i+1}"):
            c1, c2, c3, c4 = st.columns(4)
            d_atas_pond[i] = c1.number_input(f"D. Atas Pond {i+1} (m)", min_value=0.0, key=f"da_pr_{i}")
            d_bawah_pond[i] = c2.number_input(f"D. Bawah Pond {i+1} (m)", min_value=0.0, key=f"db_pr_{i}")
            t_pondasis[i] = c3.number_input(f"Tinggi Pond {i+1} (m)", min_value=0.0, key=f"tp_pr_{i}")
            d_tanks[i] = c4.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, key=f"dt_pr_{i}")

    st.markdown("### 🛡️ Safety Distance")
    col_sd1, col_sd2 = st.columns(2)
    d_safety_1 = col_sd1.number_input("Diameter Tangki Pembanding 1 (m)", min_value=0.0, key="sd_d1_pr")
    d_safety_2 = col_sd2.number_input("Diameter Tangki Pembanding 2 (m)", min_value=0.0, key="sd_d2_pr")
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_pr")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_pr")

    if st.button("💾 HITUNG", type="primary", key="btn_pr"):
        if panjang == 0 or lebar == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal)
            
            vol_pond_tank = 0
            for i in range(5):
                vol_pond_tank += (math.pi * ((d_bawah_pond[i]/2)**2) * t_pondasis[i]) + \
                                 (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            status = "✓ COMPLY" if vol_efektif_bund > (kapasitas_tank_besar * 1.1) and tinggi_dinding <= 1.8 else "✗ NON COMPLY"

            max_d_s = max(d_safety_1, d_safety_2)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
            tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
            tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else 2.0) * d_safety_1), 2)

            st.markdown("### 📈 HASIL PERHITUNGAN")
            res1, res2, res3 = st.columns(3)
            res1.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
            res1.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            res2.metric("Volume Efektif (m³)", f"{vol_efektif_bund:.2f}")
            res2.metric("Status Compliance", status)
            res3.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            res3.metric("Tank to Building (m)", f"{tank_to_build}")
            res3.metric("Tank to Property (m)", f"{tank_to_property}")
