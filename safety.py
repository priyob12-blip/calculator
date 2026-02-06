import streamlit as st
import math

# Konfigurasi Halaman
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; padding: 5rem 2rem;
        border-radius: 20px; text-align: center; color: white; margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1);
    }
    .main-banner h1 { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #00f2ff; }
    .tagline { background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-banner'><h1>BundSafe Tank Analytics</h1><p>Bundwall & Storage Tank Safety Calculator</p><div class='tagline'>Standardized by NFPA 30 | HSSE SULAWESI </div></div>", unsafe_allow_html=True)

# --- GLOBAL VARIABLES (PENTING: Agar tidak NameError) ---
d_atas_pond = [0.0] * 5
d_bawah_pond = [0.0] * 5
t_pondasis = [0.0] * 5
d_tanks = [0.0] * 5

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

st.markdown("---")

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    c1, c2, c3 = st.columns(3)
    panjang_luar = c1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar_tr")
    lebar_luar = c2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar_tr")
    tinggi_dinding = c3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding_tr")
    
    st.markdown("### 🧱 Dimensi Dinding")
    c4, c5, c6 = st.columns(3)
    lebar_atas = c4.number_input("Lebar Atas Dinding (m)", min_value=0.0, key="lebar_atas_tr")
    lebar_bawah = c5.number_input("Lebar Bawah Dinding (m)", min_value=0.0, key="lebar_bawah_tr")
