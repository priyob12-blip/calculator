import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Safety Tangki", layout="wide")

st.title("🛢️ Kalkulator Safety Tangki")
st.markdown("---")

shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"])

if st.button("🔄 RESET"):
    st.rerun()

st.markdown("---")

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    # Input bundwall (C5,C6,C7)
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, value=50.0)  # C5
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, value=50.0)      # C6
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0) # C7
    
    # Input dimensi dinding (C9,C10)
    col4, col5 = st.columns(2)
    lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0, value=0.5)       # C9
    lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0, value=1.0)      # C10
    
    # Kapasitas (C11 KL)
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    # 5 Tangki: C13=dpond1, C14=tpond1, C15=dtank1; C17=dpond2,... C19=dtank2 dst
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    d_pondasis = [0]*5
    t_pondasis = [0]*5
    d_tanks = [0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            d_pondasis[i] = col1.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            t_pondasis[i] = col2.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            d_tanks[i] = col3.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])  # E10
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])  # E11
    
    if st.button("💾 HITUNG", type="primary"):
        # Vol Bruto Trapesium EXCEL PERSIS (C34?)
        term1_inner = (panjang_luar-(lebar_bawah*2)) + (panjang_luar-((lebar_atas+((lebar_bawah-lebar_atas)/2))*2))
        term1 = ((term1_inner/2)*tinggi_dinding)*(lebar_luar-(tinggi_dinding*2))
        term2_inner = (tinggi_dinding*((lebar_bawah-lebar_atas)/2))/2
        term2 = (term2_inner*(panjang_luar-((lebar_atas+((lebar_bawah-lebar_atas)/4))*2)))*2
        vol_bruto = term1 + term2  # C34
        
        # Vol Pond+Tank EXCEL PERSIS 10 terms (C35?)
        vol_pond_tank = 0
        for i in range(5):
            vol_pond_tank += (math.pi * ((d_pondasis[i]/2)**2) * t_pondasis[i]) + \
                             (math.pi * ((d_tanks[i]/2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
        
        vol_efektif_bund = vol_bruto - vol_pond_tank  # =C34-C35
        
        # Status EXCEL PERSIS (C37 < C39 dll)
        if vol_pond_tank < vol_efektif_bund:
            status = "✗ NON COMPLY - Volume bund kurang"
        elif tinggi_dinding > 1.8:
            status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
        else:
            status = "✓ COMPLY - AMAN" if vol_pond_tank >= vol_efektif_bund else "CHECK DATA"
        
        # Shell to Shell: IF(MAX(C15,C19)<=45, (1/6)*(C15+C19), (1/3)*(C15+C19))
        c15 = d_tanks[0]  # Tank 1
        c19 = d_tanks[1]  # Tank 2
        shell_to_shell = (1/6)*(c15 + c19) if max(c15, c19) <= 45 else (1/3)*(c15 + c19)
        
        # Tank to Building: ROUND(MAX(1.5, IF(E11="Floating Roof", 1/6, IF(E10="Proteksi", 1/6, 1/3)) * C15), 2)
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * c15), 2)
        
        # Tank to Property: ROUND(MAX(1.5, IF(E11="Floating Roof", IF(E10="Proteksi", 1/2, 1), IF(E10="Proteksi", 1/2, 2)) * C15), 2)
        if jenis_tank == "Floating Roof":
            factor_prop = 0.5 if proteksi == "Proteksi" else 1
        else:
            factor_prop = 0.5 if proteksi == "Proteksi" else 2
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

else:  # Persegi - sama layout, rumus berbeda
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0, value=50.0)
    lebar = col2.number_input("Lebar (m)", min_value=0.0, value=50.0)
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)
    
    col4, col5 = st.columns(2)
    lebar_dinding1 = col4.number_input("Lebar Dinding 1 (m)", min_value=0.0, value=1.0)
    lebar_dinding2 = col5.number_input("Lebar Dinding 2 (m)", min_value=0.0, value=1.0)
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    d_pondasis = [0]*5
    t_pondasis = [0]*5
    d_tanks = [0]*5
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            d_pondasis[i] = col1.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            t_pondasis[i] = col2.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            d_tanks[i] = col3.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
    if st.button("💾 HITUNG", type="primary"):
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
        c19 = d_tanks[1]
        shell_to_shell = (1/6)*(c15 + c19) if max(c15, c19) <= 45 else (1/3)*(c15 + c19)
        
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * c15), 2)
        
        factor_prop = 0.5 if jenis_tank == "Floating Roof" and proteksi == "Proteksi" else \
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


