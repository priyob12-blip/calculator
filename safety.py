import streamlit as st
import math
import numpy as np

st.set_page_config(page_title="Kalkulator Safety Tangki", layout="wide")

st.title("🛢️ Kalkulator Safety Tangki")
st.markdown("---")

# Pilihan bentuk bundwall
shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"])

# Tombol Reset
if st.button("🔄 RESET"):
    st.rerun()

st.markdown("---")

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    
    # Input Bundwall
    col1, col2, col3 = st.columns(3)
    with col1:
        panjang_luar = st.number_input("Panjang Luar (m)", min_value=0.0, value=50.0)
    with col2:
        lebar_luar = st.number_input("Lebar Luar (m)", min_value=0.0, value=50.0)
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)
    
    # Dimensi dinding bundwall
    col4, col5 = st.columns(2)
    with col4:
        lebar_atas = st.number_input("Lebar Atas (m)", min_value=0.0, value=0.5)
    with col5:
        lebar_bawah = st.number_input("Lebar Bawah (m)", min_value=0.0, value=1.0)
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    # Input data tangki dan pondasi (5 kolom)
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            with col_t1:
                d_pondasi = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            with col_t2:
                t_pondasi = st.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            with col_t3:
                d_tank = st.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
            with col_t4:
                t_tank = st.number_input(f"Tinggi Tangki {i+1} (m)", min_value=0.0, value=12.0)
            tank_data.append((d_pondasi, t_pondasi, d_tank, t_tank))
    
    # Pilihan proteksi dan jenis tangki
    col_prot, col_roof = st.columns(2)
    with col_prot:
        proteksi = st.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    with col_roof:
        jenis_tank = st.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
    # Tombol Calculate
    if st.button("💾 HITUNG", type="primary"):
        # Rumus Volume Bruto Trapesium
        a = (panjang_luar - (lebar_bawah*2)) + (panjang_luar - ((lebar_atas + ((lebar_bawah-lebar_atas)/2))*2))
        b = a / 2 * (lebar_luar - (tinggi_dinding*2))
        c = ((tinggi_dinding * ((lebar_bawah-lebar_atas)/2)) / 2) * (panjang_luar - ((lebar_atas + ((lebar_bawah-lebar_atas)/4))*2))
        volume_bruto = b + (c * 2)
        
        # Volume Pondasi + Tank
        vol_pond_tank = 0
        d_tanks = [data[2] for data in tank_data]
        max_d_tank = max(d_tanks) if d_tanks else 0
        d_tank2 = d_tanks[1] if len(d_tanks) > 1 else max_d_tank
        
        for d_pond, t_pond, d_tank, t_tank in tank_data:
            vol_pond_tank += math.pi * ((d_pond/2)**2 * t_pond) + math.pi * ((d_tank/2)**2 * max(0, tinggi_dinding - t_pond))
        
        # Volume Efektif Bundwall
        vol_efektif_bund = kapasitas_tank_besar * 1.1
        
        # Status
        if vol_pond_tank > vol_efektif_bund:
            status = "✗ NON COMPLY - Volume bund kurang"
        elif tinggi_dinding > 1.8:
            status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
        elif vol_pond_tank >= vol_efektif_bund:
            status = "✓ COMPLY - AMAN"
        else:
            status = "CHECK DATA"
        
        # Safety Distances
        shell_to_shell = (1/6)*(max_d_tank + d_tank2) if max(max_d_tank, d_tank2) <= 45 else (1/3)*(max_d_tank + d_tank2)
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * max_d_tank), 2)
        
        factor_prop = (1/2 if jenis_tank == "Floating Roof" and proteksi == "Proteksi" else 
                      (1 if jenis_tank == "Floating Roof" else (1/2 if proteksi == "Proteksi" else 2)))
        tank_to_property = round(max(1.5, factor_prop * max_d_tank), 2)
        
        # Display Results
        st.markdown("### 📈 HASIL PERHITUNGAN")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Volume Bruto (m³)", f"{volume_bruto:.2f}")
            st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
            st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
        with col_res2:
            st.metric("Status", status)
            st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            st.metric("Tank to Building (m)", tank_to_building)
            st.metric("Tank to Property (m)", tank_to_property)

else:  # Persegi
    st.header("📏 Bundwall Persegi")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        panjang = st.number_input("Panjang (m)", min_value=0.0, value=50.0)
    with col2:
        lebar = st.number_input("Lebar (m)", min_value=0.0, value=50.0)
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)
    
    col4, col5 = st.columns(2)
    with col4:
        lebar_dinding_pjg = st.number_input("Lebar Dinding Panjang (m)", min_value=0.0, value=1.0)
    with col5:
        lebar_dinding_lbr = st.number_input("Lebar Dinding Lebar (m)", min_value=0.0, value=1.0)
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            with col_t1:
                d_pondasi = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0)
            with col_t2:
                t_pondasi = st.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
            with col_t3:
                d_tank = st.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0)
            with col_t4:
                t_tank = st.number_input(f"Tinggi Tangki {i+1} (m)", min_value=0.0, value=12.0)
            tank_data.append((d_pondasi, t_pondasi, d_tank, t_tank))
    
    col_prot, col_roof = st.columns(2)
    with col_prot:
        proteksi = st.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    with col_roof:
        jenis_tank = st.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
    if st.button("💾 HITUNG", type="primary"):
        # Rumus Volume Bruto Persegi: tinggi * (panjang - 2*lebar_dinding_pjg) * (lebar - 2*lebar_dinding_lbr)
        volume_bruto = tinggi_dinding * (panjang - 2 * lebar_dinding_pjg) * (lebar - 2 * lebar_dinding_lbr)
        
        vol_pond_tank = 0
        d_tanks = [data[2] for data in tank_data]
        max_d_tank = max(d_tanks) if d_tanks else 0
        d_tank2 = d_tanks[1] if len(d_tanks) > 1 else max_d_tank
        
        for d_pond, t_pond, d_tank, t_tank in tank_data:
            vol_pond_tank += math.pi * ((d_pond/2)**2 * t_pond) + math.pi * ((d_tank/2)**2 * max(0, tinggi_dinding - t_pond))
        
        vol_efektif_bund = kapasitas_tank_besar * 1.1
        
        if vol_pond_tank > vol_efektif_bund:
            status = "✗ NON COMPLY - Volume bund kurang"
        elif tinggi_dinding > 1.8:
            status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
        elif vol_pond_tank >= vol_efektif_bund:
            status = "✓ COMPLY - AMAN"
        else:
            status = "CHECK DATA"
        
        shell_to_shell = (1/6)*(max_d_tank + d_tank2) if max(max_d_tank, d_tank2) <= 45 else (1/3)*(max_d_tank + d_tank2)
        factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
        tank_to_building = round(max(1.5, factor_build * max_d_tank), 2)
        factor_prop = (1/2 if jenis_tank == "Floating Roof" and proteksi == "Proteksi" else 
                      (1 if jenis_tank == "Floating Roof" else (1/2 if proteksi == "Proteksi" else 2)))
        tank_to_property = round(max(1.5, factor_prop * max_d_tank), 2)
        
        st.markdown("### 📈 HASIL PERHITUNGAN")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Volume Bruto (m³)", f"{volume_bruto:.2f}")
            st.metric("Vol. Efektif Bund (m³)", f"{vol_efektif_bund:.2f}")
            st.metric("Vol. Pond+Tank (m³)", f"{vol_pond_tank:.2f}")
        with col_res2:
            st.metric("Status", status)
            st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            st.metric("Tank to Building (m)", tank_to_building)
            st.metric("Tank to Property (m)", tank_to_property)
