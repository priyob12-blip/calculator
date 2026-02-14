import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="BundSafe Tank Analytics", 
    page_icon="⚡", 
    layout="wide"
)

# --- CUSTOM CSS UNTUK UI MODERN & DESIGN KOTAK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; padding: 4rem 2rem;
        border-radius: 20px; text-align: center; color: white; margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
    }
    .main-banner h1 { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #00f2ff; text-shadow: 0 0 15px rgba(0, 242, 255, 0.6); }
    .custom-card {
        background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px; padding: 20px; margin-bottom: 25px; position: relative; overflow: hidden;
    }
    .custom-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 10px; height: 40px;
        background: #007BFF; border-radius: 0 0 10px 0;
    }
    .section-title { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 800; color: #000000; margin-bottom: 20px; padding-left: 15px; }
    .status-comply { color: #00ff88; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
    .status-noncomply { color: #ff4b4b; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; border-radius: 5px;'>Standardized by NFPA 30 | HSSE SULAWESI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FUNGSI PEMBANTU SAFETY DISTANCE ---
def estimate_cap(dia):
    # Mapping Diameter ke Kapasitas sesuai Tabel 4
    if dia <= 6.68: return 150
    elif dia <= 7.64: return 200
    elif dia <= 8.59: return 250
    elif dia <= 9.55: return 500
    elif dia <= 11.46: return 700
    elif dia <= 13.37: return 1500
    elif dia <= 15.28: return 2000
    elif dia <= 17.19: return 2500
    elif dia <= 19.10: return 5000
    elif dia <= 27.69: return 10000
    elif dia <= 30.56: return 12500
    elif dia <= 33.42: return 15000
    elif dia <= 40.11: return 20000
    elif dia <= 43.93: return 25000
    elif dia <= 48.70: return 30000
    else: return 50000

def get_nfpa_dist(cap, is_mfo):
    # Logika diperbaiki agar pas dengan range Tabel NFPA 30
    # dist_a = jarak ke fasilitas/bangunan terdekat
    # dist_b = jarak ke jalan umum
    if not is_mfo:
        if cap <= 1.045: return 1.5, 1.5
        elif cap <= 2.85: return 3.0, 1.5
        elif cap <= 45.6: return 4.5, 1.5
        elif cap <= 114.0: return 6.0, 1.5
        elif cap <= 190.0: return 9.0, 3.0
        elif cap <= 380.0: return 15.0, 4.5
        elif cap <= 1900.0: return 24.0, 7.5
        elif cap <= 3800.0: return 30.0, 10.5
        elif cap <= 7600.0: return 40.5, 13.5
        elif cap <= 11400.0: return 49.5, 16.5
        else: return 52.5, 18.0
    else: 
        if cap <= 45.6: return 1.5, 1.5
        elif cap <= 114.0: return 3.0, 1.5
        elif cap <= 190.0: return 3.0, 3.0
        elif cap <= 380.0: return 4.5, 3.0
        else: return 4.5, 4.5

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

d_atas_pond, d_bawah_pond, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5, [0.0]*5

if shape == "Trapesium":
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Trapesium</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar")
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0, key="lebar_atas")
    lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0, key="lebar_bawah")
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kapasitas")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            ct1, ct2, ct3, ct4 = st.columns(4)
            d_atas_pond[i] = ct1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_tr_{i}")
            d_bawah_pond[i] = ct2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_tr_{i}")
            t_pondasis[i] = ct3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_tr_{i}")
            d_tanks[i] = ct4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_tr_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
    cs1, cs2, cs3, cs4, cs5 = st.columns(5)
    produk = cs1.selectbox("Jenis BBM:", ["Pertalite", "Pertamax", "Solar", "Avtur", "MFO"], key="prod_tr")
    d_safety_1 = cs2.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_tr")
    d_safety_2 = cs3.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_tr")
    proteksi = cs4.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_tr")
    jenis_tank = cs5.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_tr")
    st.markdown("</div>", unsafe_allow_html=True)

else:  # Persegi
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Persegi</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0, key="p_per")
    lebar = col2.number_input("Lebar (m)", min_value=0.0, key="l_per")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_per")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    lebar_dinding = col4.number_input("Lebar Dinding (m)", min_value=0.0, key="ld1_per")
    panjang_tebal_dinding = col5.number_input("
