import streamlit as st
import math

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="BundSafe Tank Analytics", 
    page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Sulawesi_Silhouette.svg/512px-Sulawesi_Silhouette.svg.png", 
    layout="wide"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .main-banner h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        color: #00f2ff;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    .custom-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 10px; height: 40px;
        background: #007BFF;
        border-radius: 0 0 10px 0;
    }
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #000000; 
        margin-bottom: 20px;
        padding-left: 15px;
    }
    .status-comply { color: #00ff88; font-weight: bold; font-family: 'Orbitron', sans-serif; }
    .status-noncomply { color: #ff4b4b; font-weight: bold; font-family: 'Orbitron', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 3. BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; border-radius: 5px;'>Standardized by NFPA 30 | HSSE SULAWESI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. INPUT UTAMA ---
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
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0)
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0)
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0) # Penutup kurung diperbaiki
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0)
    lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0)
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Persegi</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0)
    lebar = col2.number_input("Lebar (m)", min_value=0.0)
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    lebar_dinding = col4.number_input("Lebar Dinding (m)", min_value=0.0)
    panjang_tebal_dinding = col5.number_input("Ketebalan Dinding (m)", min_value=0.0)
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0)

# --- 5. DATA TANGKI & SAFETY ---
st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
for i in range(5):
    with st.expander(f"Tangki {i+1}"):
        ct1, ct2, ct3, ct4 = st.columns(4)
        d_atas_pond[i] = ct1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"da_{i}")
        d_bawah_pond[i] = ct2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"db_{i}")
        t_pondasis[i] = ct3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"tp_{i}")
        d_tanks[i] = ct4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"dt_{i}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
cs1, cs2, cs3, cs4 = st.columns(4)
d_safety_1 = cs1.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd1")
d_safety_2 = cs2.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd2")
proteksi = cs3.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
jenis_tank = cs4.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
st.markdown("</div>", unsafe_allow_html=True
