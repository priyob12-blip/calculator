import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Safety Tangki", layout="wide")

st.title("🛢️ Kalkulator Safety Tangki")
st.markdown("---")

# Session state untuk reset ke 0
if 'reset_all' not in st.session_state:
    st.session_state.reset_all = False

shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"], key="shape_select")

if st.button("🔄 RESET"):
    st.session_state.reset_all = True
    st.rerun()

st.markdown("---")
st.session_state.reset_all = False  # Reset flag setelah rerun

def number_input_zero(label, key):
    """Number input default 0, reset jika flag true"""
    if st.session_state.reset_all:
        value = 0.0
    else:
        value = 0.0  # Selalu start dari 0
    return st.number_input(label, min_value=0.0, value=value, key=key)

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    # Input bundwall default 0
    col1, col2, col3 = st.columns(3)
    panjang_luar = number_input_zero("Panjang Luar (m)", "p_luar")  # C5
    lebar_luar = number_input_zero("Lebar Luar (m)", "l_luar")      # C6
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_dinding") # C7
    
    # Dimensi dinding default 0
    col4, col5 = st.columns(2)
    lebar_atas = number_input_zero("Lebar Atas (m)", "lebar_atas") # C9
    lebar_bawah = number_input_zero("Lebar Bawah (m)", "lebar_bawah") # C10
    
    # Kapasitas default 0
    kapasitas_tank_besar = number_input_zero("Kapasitas Tangki Terbesar (KL)", "kapasitas")
    
    # 5 Tangki default 0
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    d_pondasis = [0]*5
    t_pondasis = [0]*5
    d_tanks = [0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            d_pondasis[i] = number_input_zero(f"Diameter Pondasi {i+1} (m)", f"dpond_{i}")
            t_pondasis[i] = number_input_zero(f"Tinggi Pondasi {i+1} (m)", f"tpond_{i}")
            d_tanks[i] = number_input_zero(f"Diameter Tangki {i+1} (m)", f"dtank_{i}")
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], index=0, key="prot")
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], index=0, key="jenis")
    
    if st.button("💾 HITUNG", type="primary"):
        if all([panjang_luar==0, lebar_luar==0, tinggi_dinding==0]):  # Skip jika semua 0
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
            
            # Status EXCEL
            if vol_pond_tank < vol_efektif_bund:
                status = "✗ NON COMPLY - Volume bund kurang"
            elif tinggi_dinding > 1.8:
                status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
            else:
                status = "✓ COMPLY - AMAN" if vol_pond_tank >= vol_efektif_bund else "CHECK DATA"
            
            # Distances pakai C15 (tank1), C19 (tank2)
            c15 = d_tanks[0]
            c19 = d_tanks[1] if len(d_tanks)>1 else 0
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

else:  # Persegi - sama, default 0 semua
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    panjang = number_input_zero("Panjang (m)", "p_per")
    lebar = number_input_zero("Lebar (m)", "l_per")
    tinggi_dinding = number_input_zero("Tinggi Dinding (m)", "t_per")
    
    col4, col5 = st.columns(2)
    lebar_dinding1 = number_input_zero("Lebar Dinding 1 (m)", "ld1_per")
    lebar_dinding2 = number_input_zero("Lebar Dinding 2 (m)", "ld2_per")
    
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
            vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding1) * (lebar - 2*lebar_dinding2)
            
            vol_pond_tank = 0
            for i in range(5):
                vol_pond_tank += (math.pi * ((d_pondasis[i]/2)**2) * t_pondasis[i]) + \
                                 (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
            
            vol_efektif_bund = vol_bruto - vol_pond_tank
            
            if vol_pond_tank < vol_efektif_bund:
                status = "✗ NON COMPLY - Volume bund kurang"
            elif tinggi_dinding > 1.8:
                status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
            else:
                status = "✓ COMPLY - AMAN" if vol_pond_tank >= vol_efektif_bund else "CHECK DATA"
            
            c15 = d_tanks[0]
            c19 = d_tanks[1] if len(d_tanks)>1 else 0
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



