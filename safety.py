import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK UI MODERN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .main-banner h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        margin: 0;
        color: #00f2ff;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }
    .tagline {
        background: #ffcc00;
        color: #000;
        padding: 5px 15px;
        font-weight: bold;
        text-transform: uppercase;
        border-radius: 5px;
        display: inline-block;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div class='tagline'>Standardized by NFPA 30 | HSSE SULAWESI</div>
</div>
""", unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def number_input_zero(label, key, val=0.0):
    return st.number_input(label, min_value=0.0, value=val, key=key)

# --- INPUT UTAMA ---
shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"], key="shape_select")

if st.button("🔄 RESET", type="secondary"):
    st.rerun()

st.markdown("---")

# --- LOGIKA TRAPESIUM ---
if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    col1, col2, col3 = st.columns(3)
    panjang_luar = number_input_zero("Panjang Luar (L) (m)", "p_luar", 32.2)
    lebar_luar = number_input_zero("Lebar Luar (W) (m)", "l_luar", 32.2)
    tinggi_dinding = number_input_zero("Tinggi Dinding (h) (m)", "t_dinding", 2.0)
    
    st.markdown("### 🧱 Dimensi Dinding")
    col4, col5 = st.columns(2)
    lebar_atas = number_input_zero("Lebar Atas Dinding (a) (m)", "lebar_atas", 0.6)
    lebar_bawah = number_input_zero("Lebar Bawah Dinding (b) (m)", "lebar_bawah", 2.2)
    
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kapasitas", 1500.0)
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    d_pondasis, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            c1, c2, c3 = st.columns(3)
            d_pondasis[i] = c1.number_input(f"Diameter Pondasi {i+1} (m)", key=f"

