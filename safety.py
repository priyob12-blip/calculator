import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK UI MODERN & DESIGN KOTAK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Banner Utama */
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

    /* Card Section dengan Slice Biru */
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
        top: 0;
        left: 0;
        width: 10px;
        height: 40px;
        background: #007BFF;
        border-radius: 0 0 10px 0;
    }

    /* JUDUL HITAM & BOLD */
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #000000; 
        margin-bottom: 20px;
        padding-left: 15px;
    }

    /* Status Label Styling */
    .status-comply {
        color: #00ff88;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    .status-noncomply {
        color: #ff4b4b;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
    }
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

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

def number_input_zero(label, key):
    return st.number_input(label, min_value=0.0, value=0.0, key=key)

# Persiapan List Data Tangki
d_atas_pond, d_bawah_pond, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5, [0.0]*5

# UI Logic berdasarkan Shape
if shape == "Trapesium":
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Trapesium</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar")
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min
