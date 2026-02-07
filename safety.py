import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK UI MODERN & LIST BIRU ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Banner Utama */
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
        text-align: center;
    }

    .main-banner p {
        font-family: 'Inter', sans-serif;
        font-size: 1.4rem;
        margin: 10px 0;
        text-align: center;
    }

    .tagline-container {
        text-align: center;
        margin-top: 10px;
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

    /* --- STYLING LIST BIRU DI SAMPING JUDUL --- */
    .section-header {
        border-left: 6px solid #007BFF; /* Garis List Biru */
        padding-left: 15px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    .section-header h2, .section-header h3 {
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div class='tagline-container'>
        <div class='tagline'>Standardized by NFPA 30 | HSSE SULAWESI </div>
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

# Persiapan List Data Tangki
d_atas_pond = [0.0]*5
d_bawah_pond = [0.0]*5
t_pondasis = [0.0]*5
d_tanks = [0.0]*5

if shape == "Trapesium":
    st.markdown("<div class='section-header'><h2>Bundwall Trapesium</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    panjang_luar = number_input_zero("Panjang Luar (m)", "p_luar")
    lebar_luar = number_input_zero("Lebar Luar (m)", "l_luar")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_dinding")
    
    st.markdown("<div class='section-header'><h3>Dimensi Dinding</h3></div>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    lebar_atas = number_input_zero("Lebar Atas (m)", "lebar_atas")
    lebar_bawah = number_input_zero("Lebar Bawah (m)", "lebar_bawah")
    
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kapasitas")
    
    st.markdown("<div class='section-header'><h3>Data Tangki & Pondasi (5 Unit)</h3></div>", unsafe_allow_html=True)
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            d_atas_pond[i] = col_t1.number_input(f"D. Atas Pondasi {i+1} (m)", min_value=0.0, key=f"d_atas_tr_{i}")
            d_bawah_pond[i] = col_t2.number_input(f"D. Bawah Pondasi {i+1} (m)", min_value=0.0, key=f"d_bawah_tr_{i}")
            t_pondasis[i] = col_t3.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, key=f"t_pond_tr_{i}")
            d_tanks[i] = col_t4.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, key=f"d_tank_tr_{i}")

    st.markdown("---")
    st.markdown("<div class='section-header'><h3>Safety Distance</h3></div>", unsafe_allow_html=True)
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
            t1_a = (panjang_luar - (2 * lebar_bawah))
            t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
            term1 = ((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))
            s_val = (lebar_bawah - lebar_atas) / 2
            term2 = ((lebar_bawah * s_val) / 2) * (panjang_luar - (s_val + lebar_bawah)) * 2
            vol_bruto = term1 + term2

            vol_pond_tank = 0
            for i in range(5):
                r_atas = d_atas_pond[i] / 2
                r_bawah = d_bawah_pond[i] / 2
                v_pondasi = (1/3) * math.pi * t_pondasis[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
                r_tank = d_tanks[i] / 2
                tinggi_tank_tenggelam = max(0, tinggi_dinding - t_pondasis[i])
                v_tank = math.pi * (r_tank**2) * tinggi_tank_tenggelam
                vol_pond_tank += (v_pondasi + v_tank)
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            vol_min = kapasitas_tank_besar * 1.0  # Rumus: Tangki Terbesar * 100%
            
            status = "✓ COMPLY - AMAN" if vol_efektif_bund > kapasitas_tank_besar * 1.1 and tinggi_dinding <= 1.8 else "✗ NON COMPLY"

            max_d_s = max(d_safety_1, d_safety_2)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
            tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
            tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else (1.0 if jenis_tank == "Floating Roof" else 2.0)) * d_safety_1), 2)

            st.markdown("### 📈 HASIL PERHITUNGAN")
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            with col_res1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col_res2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Volume Minimum (m³)", f"{vol_min:.2f}")
            with col_res3:
                st.metric("Status Safety", status)
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            with col_res4:
                st.metric("Tank to Building (m)", f"{tank_to_build}")
                st.metric("Tank to Property (m)", f"{tank_to_property}")

else:  # Persegi
    st.markdown("<div class='section-header'><h2>Bundwall Persegi</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    panjang = number_input_zero("Panjang (m)", "p_per")
    lebar = number_input_zero("Lebar (m)", "l_per")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_per")
    
    st.markdown("<div class='section-header'><h3>Dimensi Dinding</h3></div>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    lebar_dinding = number_input_zero("Lebar Dinding (m)", "ld1_per")
    panjang_tebal_dinding = number_input_zero("Ketebalan Dinding (m)", "ld2_per")
    
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kap_per")
    
    st.markdown("<div class='section-header'><h3>Data Tangki & Pondasi (5 Unit)</h3></div>", unsafe_allow_html=True)
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            d_atas_pond[i] = col_p1.number_input(f"D. Atas Pondasi {i+1} (m)", min_value=0.0, key=f"d_atas_pr_{i}")
            d_bawah_pond[i] = col_p2.number_input(f"D. Bawah Pondasi {i+1} (m)", min_value=0.0, key=f"d_bawah_pr_{i}")
            t_pondasis[i] = col_p3.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, key=f"t_pond_pr_{i}")
            d_tanks[i] = col_p4.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, key=f"d_tank_pr_{i}")

    st.markdown("<div class='section-header'><h3>Safety Distance</h3></div>", unsafe_allow_html=True)
    col_sd1, col_sd2 = st.columns(2)
    d_safety_1 = col_sd1.number_input("Diameter Tangki Pembanding 1 (m)", min_value=0.0, key="sd_d1_pr")
    d_safety_2 = col_sd2.number_input("Diameter Tangki Pembanding 2 (m)", min_value=0.0, key="sd_d2_pr")
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_per_sd")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_per_sd")

    if st.button("💾 HITUNG", type="primary", key="btn_per"):
        if panjang == 0 or lebar == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal_dinding)
            
            vol_pond_tank = 0
            for i in range(5):
                r_atas = d_atas_pond[i] / 2
                r_bawah = d_bawah_pond[i] / 2
                v_pondasi = (1/3) * math.pi * t_pondasis[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
                r_tank = d_tanks[i] / 2
                tinggi_tank_tenggelam = max(0, tinggi_dinding - t_pondasis[i])
                v_tank = math.pi * (r_tank**2) * tinggi_tank_tenggelam
                vol_pond_tank += (v_pondasi + v_tank)
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            vol_min = kapasitas_tank_besar * 1.0 # Rumus: Tangki Terbesar * 100%
            
            status = "✓ COMPLY - AMAN" if vol_efektif_bund > kapasitas_tank_besar * 1.1 and tinggi_dinding <= 1.8 else "✗ NON COMPLY"

            # Hitungan safety distance untuk persegi (menggunakan logika yang sama agar variabel terdefinisi)
            max_d_s = max(d_safety_1, d_safety_2)
            shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
            f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
            tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
            tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else (1.0 if jenis_tank == "Floating Roof" else 2.0)) * d_safety_1), 2)

            st.markdown("### 📈 HASIL PERHITUNGAN")
            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            with col_res1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col_res2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Volume Minimum (m³)", f"{vol_min:.2f}")
            with col_res3:
                st.metric("Status Safety", status)
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            with col_res4:
                st.metric("Tank to Building (m)", f"{tank_to_build}")
                st.metric("Tank to Property (m)", f"{tank_to_property}")
