import streamlit as st
import math

st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK VISUAL PREMIUM ---
st.markdown("""
<style>
    /* Styling untuk seluruh halaman, agar latar belakang cocok dengan banner */
    body {
        background-color: #0f1116; /* Warna latar belakang gelap */
        color: #e0e0e0;
    }
    .stApp {
        background-color: #0f1116; /* Menyamakan warna latar belakang Streamlit */
    }

    /* Banner Utama dengan gambar background yang dramatis */
    .main-banner {
        background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), 
                        url('https://images.unsplash.com/photo-1579547621810-5491104e793e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80'); /* Gambar tangki dengan sunset */
        background-size: cover;
        background-position: center;
        padding: 6rem 2rem; /* Padding lebih besar */
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem; /* Margin lebih besar */
        box-shadow: 0 15px 50px rgba(0,0,0,0.6); /* Shadow lebih kuat */
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden; /* Pastikan tidak ada overflow dari pseudo-element */
    }

    /* Efek overlay futuristik (pseudo-element) */
    .main-banner::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0) 70%);
        pointer-events: none;
    }

    .main-banner h1 {
        font-size: 4rem; /* Ukuran font lebih besar */
        margin: 0;
        font-weight: 900;
        letter-spacing: -2px;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.6);
        background: linear-gradient(45deg, #a4eaff, #80c8ff); /* Gradient untuk judul utama */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block; /* Penting untuk gradient teks */
    }
    .main-banner p {
        font-size: 1.5rem; /* Ukuran font lebih besar */
        margin: 18px 0;
        opacity: 0.9;
        font-weight: 300;
        color: #f0f2f6;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    .main-banner .tagline {
        font-size: 1.2rem;
        margin: 0;
        font-style: italic;
        color: #ffcc00; /* Kuning terang */
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }
    .main-banner .separator {
        height: 4px;
        background: linear-gradient(90deg, transparent, #ffcc00, transparent);
        width: 120px;
        margin: 25px auto;
        border-radius: 2px;
    }

    /* Judul Dimensi Dinding dengan gaya futuristik */
    .dimensi-header {
        background: linear-gradient(90deg, #1f2a3a 0%, #2a3e54 50%, #3a5871 100%);
        padding: 18px 30px;
        border-radius: 15px;
        margin: 3rem 0 2rem 0; /* Margin lebih besar */
        color: white;
        border-left: 8px solid #00aaff; /* Aksen biru terang */
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .dimensi-header h3 {
        margin: 0;
        font-size: 1.7rem; /* Ukuran font lebih besar */
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #e0f2f7;
    }
    .dimensi-header .icon {
        font-size: 2rem;
        color: #00aaff;
    }

    /* Styling umum untuk input dan tombol */
    .stSelectbox > div > div {
        background-color: #1a1f26;
        color: #e0e0e0;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stNumberInput > div > div > input {
        background-color: #1a1f26;
        color: #e0e0e0;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #00aaff;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #007bff;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# --- TAMPILAN BANNER ATAS ---
st.markdown("""
<div class='main-banner'>
    <h1>🛡️ BundSafe Tank Analytics</h1>
    <p>Professional Spill Containment & Storage Tank Safety Calculator</p>
    <div class='separator'></div>
    <p class='tagline'>Standardized by NFPA 30 | Engineered By. PBJ</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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

