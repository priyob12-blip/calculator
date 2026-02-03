import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK BANNER TANGKI & UI MODERN ---
st.markdown("""
<style>
    /* Mengatur font agar lebih modern */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        /* Gambar Background Tangki Timbun (Bukan Rumput/Gunung) */
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), 
        url('https://images.unsplash.com/photo-1581094271901-8022df4466f9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        padding: 5rem 3rem;
        border-radius: 20px;
        text-align: left;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border-bottom: 5px solid #00f2ff;
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
        <div style='font-size: 4rem;'>🛡️</div>
        <div>
            <h1>BundSafe Tank Analytics</h1>
            <p>Professional Spill Containment & Storage Tank Safety Calculator</p>
            <div class='tagline'>Standardized by NFPA 30 | Engineered By. PBJ</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SISA KODINGAN (INPUT & LOGIC) ---

st.markdown("---")
shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"], key="shape_select")

if st.button("🔄 RESET", type="secondary"):
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
    d_pondasis = [0]*5
    t_pondasis = [0]*5
    d_tanks = [0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            d_pondasis[i] = number_input_zero(f"Diameter Pondasi {i+1} (m)", f"dpond_tr_{i}")
            t_pondasis[i] = number_input_zero(f"Tinggi Pondasi {i+1} (m)", f"tpond_tr_{i}")
            d_tanks[i] = number_input_zero(f"Diameter Tangki {i+1} (m)", f"dtank_tr_{i}")
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_tr")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_tr")
    
    if st.button("💾 HITUNG", type="primary"):
        if panjang_luar == 0 or lebar_luar == 0 or tinggi_dinding == 0:
            st.warning("⚠️ Masukkan data bundwall terlebih dahulu!")
        else:
            # Vol Bruto EXCEL PERSIS
            term1_inner = (panjang_luar-(lebar_bawah*2)) + (panjang_luar-((lebar_atas+((lebar_bawah-lebar_atas)/2))*2))
            term1 = ((term1_inner/2)*tinggi_dinding)*(lebar_luar-(tinggi_dinding*2))
            term2_inner = (tinggi_dinding*((lebar_bawah-lebar_atas)/2))/2
            term2 = (term2_inner*(panjang_luar-((lebar_atas+((lebar_bawah-lebar_atas)/4))*2)))*2
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

            
            c15 = d_tanks[0]
            c19 = d_tanks[1] if len(d_tanks)>1 else c15
            shell_to_shell = (1/6)*(c15 + c19) if max(c15, c19) <= 45 else (1/3)*(c15 + c19)
            
            factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
            tank_to_building = round(max(1.5, factor_build * c15), 2)
            
            factor_prop = 0.5 if (jenis_tank == "Floating Roof" and proteksi == "Proteksi") else \
                          1 if jenis_tank == "Floating Roof" else (0.5 if proteksi == "Proteksi" else 2)
            tank_to_property = round(max(1.5, factor_prop * c15), 2)
            
            st.markdown("### 📈 HASIL PERHITUNGAN")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Status", status)
            with col3:
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
                st.metric("Tank to Building (m)", tank_to_building)
                st.metric("Tank to Property (m)", tank_to_property)

else:  # Persegi
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    panjang = number_input_zero("Panjang (m)", "p_per")
    lebar = number_input_zero("Lebar (m)", "l_per")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_per")
    
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
            
            c15 = d_tanks[0]
            c19 = d_tanks[1] if len(d_tanks)>1 else c15
            shell_to_shell = (1/6)*(c15 + c19) if max(c15, c19) <= 45 else (1/3)*(c15 + c19)
            
            factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
            tank_to_building = round(max(1.5, factor_build * c15), 2)
            
            factor_prop = 0.5 if (jenis_tank == "Floating Roof" and proteksi == "Proteksi") else \
                          1 if jenis_tank == "Floating Roof" else (0.5 if proteksi == "Proteksi" else 2)
            tank_to_property = round(max(1.5, factor_prop * c15), 2)
            
            st.markdown("### 📈 HASIL PERHITUNGAN")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Volume Bruto (m³)", f"{vol_bruto:.2f}")
                st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
            with col2:
                st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
                st.metric("Status", status)
            with col3:
                st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
                st.metric("Tank to Building (m)", tank_to_building)
                st.metric("Tank to Property (m)", tank_to_property)

