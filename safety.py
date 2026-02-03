import streamlit as st
import math

st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK VISUAL PREMIUM ---
st.markdown("""
<style>
    /* Banner Utama dengan nuansa Industri High-End */
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1542224566-6e85f2e6772f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 5rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Judul Dimensi Dinding Premium */
    .dimensi-header {
        background: linear-gradient(90deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 15px 25px;
        border-radius: 12px;
        margin: 2.5rem 0 1.5rem 0;
        color: white;
        border-left: 8px solid #ffcc00; /* Aksen Kuning */
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .dimensi-header h3 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- TAMPILAN BANNER ATAS ---
st.markdown("""
<div class='main-banner'>
    <h1 style='font-size: 3.8rem; margin: 0; font-weight: 900; letter-spacing: -1px;'>
        🛡️ BundSafe Tank Analytics
    </h1>
    <p style='font-size: 1.4rem; margin: 15px 0; opacity: 0.85; font-weight: 400; color: #f0f2f6;'>
        Professional Spill Containment & Storage Tank Safety Calculator
    </p>
    <div style='height: 3px; background: #ffcc00; width: 80px; margin: 20px auto;'></div>
    <p style='font-size: 1.2rem; margin: 0; font-style: italic; color: #ffffff;'>
        Standardized by NFPA 30 | HSSE SULAWESI
    </p>
</div>
""", unsafe_allow_html=True)

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

