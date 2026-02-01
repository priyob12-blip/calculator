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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        panjang_luar = st.number_input("Panjang Luar (m)", min_value=0.0, value=50.0)  # C5
    with col2:
        lebar_luar = st.number_input("Lebar Luar (m)", min_value=0.0, value=50.0)      # C6
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)  # C7
    
    col4, col5 = st.columns(2)
    with col4:
        lebar_atas = st.number_input("Lebar Atas (m)", min_value=0.0, value=0.5)      # C9
    with col5:
        lebar_bawah = st.number_input("Lebar Bawah (m)", min_value=0.0, value=1.0)     # C10
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)  # C11 -> KL
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                d_pond1 = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            with col2:
                t_pond1 = st.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            with col3:
                d_tank1 = st.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
            tank_data.append((d_pond1, t_pond1, d_tank1))
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
    if st.button("💾 HITUNG", type="primary"):
        # RUMUS EXCEL PERSIS: (((((C5-(C10*2))+(C5-((C9+((C10-C9)/2))*2)))/2*C7)*(C6-(C7*2)))+((((C7*((C10-C9)/2))/2)*(C5-((C9+((C10-C9)/4))*2)))*2)
        term1_inner = (panjang_luar - (lebar_bawah * 2)) + (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
        term1 = ((term1_inner / 2) * tinggi_dinding) * (lebar_luar - (tinggi_dinding * 2))
        term2_inner = (tinggi_dinding * ((lebar_bawah - lebar_atas) / 2)) / 2
        term2 = (term2_inner * (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 4)) * 2))) * 2
        volume_bruto = term1 + term2  # C37?
        
        # Volume Pond+Tank (sum 10 PI terms, pakai tinggi_dinding sebagai ref atas)
        vol_pond_tank = 0
        d_tanks = [data[2] for data in tank_data]
        max_d_tank = max(d_tanks) if d_tanks else 0
        d_tank2 = d_tanks[1] if len(d_tanks) > 1 else max_d_tank
        
        for d_pond, t_pond, d_tank in tank_data:
            vol_pond_tank += (math.pi * ((d_pond / 2)**2) * t_pond) + (math.pi * ((d_tank / 2)**2) * max(0, tinggi_dinding - t_pond))
        
        vol_efektif_bund = kapasitas_tank_besar * 1.1  # C39
        
        # Status IF persis Excel
        if vol_pond_tank < vol_efektif_bund:
            status = "✗ NON COMPLY - Volume bund kurang"
        elif tinggi_dinding > 1.8:
            status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
        elif vol_pond_tank >= vol_efektif_bund:
            status = "✓ COMPLY - AMAN"
        else:
            status = "CHECK DATA"
        
        # Shell to Shell: IF(MAX(C15,C19)<=45; (1/6)*(C15+C19); (1/3)*(C15+C19))
        shell_to_shell = (1/6) * (max_d_tank + d_tank2) if max(max_d_tank, d_tank2) <= 45 else (1/3) * (max_d_tank + d_tank2)
        
        # Tank to Building: ROUND(MAX(1,5; IF(E11="Floating Roof"; 1/6; IF(E10="Proteksi"; 1/6; 1/3)) * C15); 2)
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * max_d_tank), 2)
        
        # Tank to Property: ROUND(MAX(1,5; IF(E11="Floating Roof"; IF(E10="Proteksi"; 1/2; 1); IF(E10="Proteksi"; 1/2; 2)) * C15); 2)
        if jenis_tank == "Floating Roof":
            factor_prop = 0.5 if proteksi == "Proteksi" else 1
        else:
            factor_prop = 0.5 if proteksi == "Proteksi" else 2
        tank_to_property = round(max(1.5, factor_prop * max_d_tank), 2)
        
        st.markdown("### 📈 HASIL PERHITUNGAN")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Volume Bruto (m³)", f"{volume_bruto:.2f}")
            st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
            st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
        with col2:
            st.metric("Status", status)
            st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            st.metric("Tank to Building (m)", tank_to_building)
            st.metric("Tank to Property (m)", tank_to_property)

else:  # Persegi
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        panjang = st.number_input("Panjang (m)", min_value=0.0, value=50.0)  # C5
    with col2:
        lebar = st.number_input("Lebar (m)", min_value=0.0, value=50.0)      # C6
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)  # C7
    
    col4, col5 = st.columns(2)
    with col4:
        lebar_dinding = st.number_input("Lebar Dinding (m)", min_value=0.0, value=1.0)  # C9/C10 equivalent
    with col5:
        _ = st.empty()  # Placeholder
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                d_pond1 = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            with col2:
                t_pond1 = st.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            with col3:
                d_tank1 = st.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
            tank_data.append((d_pond1, t_pond1, d_tank1))
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
    if st.button("💾 HITUNG", type="primary"):
        # Rumus Persegi: =C7 * (C5 - 2*C10) * (C6 - 2*C9) -> pakai lebar_dinding sama
        volume_bruto = tinggi_dinding * (panjang - 2 * lebar_dinding) * (lebar - 2 * lebar_dinding)
        
        vol_pond_tank = 0
        d_tanks = [data[2] for data in tank_data]
        max_d_tank = max(d_tanks) if d_tanks else 0
        d_tank2 = d_tanks[1] if len(d_tanks) > 1 else max_d_tank
        
        for d_pond, t_pond, d_tank in tank_data:
            vol_pond_tank += (math.pi * ((d_pond / 2)**2) * t_pond) + (math.pi * ((d_tank / 2)**2) * max(0, tinggi_dinding - t_pond))
        
        vol_efektif_bund = kapasitas_tank_besar * 1.1
        
        if vol_pond_tank < vol_efektif_bund:
            status = "✗ NON COMPLY - Volume bund kurang"
        elif tinggi_dinding > 1.8:
            status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
        elif vol_pond_tank >= vol_efektif_bund:
            status = "✓ COMPLY - AMAN"
        else:
            status = "CHECK DATA"
        
        shell_to_shell = (1/6) * (max_d_tank + d_tank2) if max(max_d_tank, d_tank2) <= 45 else (1/3) * (max_d_tank + d_tank2)
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * max_d_tank), 2)
        factor_prop = 0.5 if (jenis_tank == "Floating Roof" and proteksi == "Proteksi") else (1 if jenis_tank == "Floating Roof" else (0.5 if proteksi == "Proteksi" else 2))
        tank_to_property = round(max(1.5, factor_prop * max_d_tank), 2)
        
        st.markdown("### 📈 HASIL PERHITUNGAN")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Volume Bruto (m³)", f"{volume_bruto:.2f}")
            st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
            st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
        with col2:
            st.metric("Status", status)
            st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            st.metric("Tank to Building (m)", tank_to_building)
            st.metric("Tank to Property (m)", tank_to_property)
