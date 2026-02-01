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
        panjang_luar = st.number_input("Panjang Luar (m)", min_value=0.0, value=50.0, key="p_luar_trap")
    with col2:
        lebar_luar = st.number_input("Lebar Luar (m)", min_value=0.0, value=50.0, key="l_luar_trap")
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0, key="t_dinding_trap")
    
    # Dimensi dinding bundwall
    col4, col5 = st.columns(2)
    with col4:
        lebar_atas = st.number_input("Lebar Atas (m)", min_value=0.0, value=0.5, key="lebar_atas_trap")
    with col5:
        lebar_bawah = st.number_input("Lebar Bawah (m)", min_value=0.0, value=1.0, key="lebar_bawah_trap")
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0, key="kap_tank_trap")
    
    # Input data tangki dan pondasi (5 kolom)
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            with col_t1:
                d_pondasi = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0, key=f"d_pond{i}_trap")
            with col_t2:
                t_pondasi = st.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0, key=f"t_pond{i}_trap")
            with col_t3:
                d_tank = st.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0, key=f"d_tank{i}_trap")
            with col_t4:
                t_tank = st.number_input(f"Tinggi Tangki {i+1} (m)", min_value=0.0, value=12.0, key=f"t_tank{i}_trap")
            tank_data.append((d_pondasi, t_pondasi, d_tank, t_tank))
    
    # Pilihan proteksi dan jenis tangki
    col_prot, col_roof = st.columns(2)
    with col_prot:
        proteksi = st.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_trap")
    with col_roof:
        jenis_tank = st.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_trap")
    
    # Tombol Calculate
    if st.button("💾 HITUNG", type="primary"):
        # Rumus Volume Bruto (C5=panjang_luar, C6=lebar_luar, C7=tinggi_dinding, C9=lebar_atas, C10=lebar_bawah)
        term1 = ((panjang_luar - (lebar_bawah * 2)) + (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))) / 2 * (lebar_luar - (tinggi_dinding * 2))
        term2 = (((tinggi_dinding * ((lebar_bawah - lebar_atas) / 2)) / 2) * (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 4)) * 2))) * 2
        volume_bruto = term1 + term2
        
        # Volume Pondasi dan Tank
        vol_pond_tank = 0
        d_tanks = [data[2] for data in tank_data]  # Diameter tanks
        max_d_tank = max(d_tanks) if d_tanks else 0
        
        for i, (d_pond, t_pond, d_tank, t_tank) in enumerate(tank_data):
            vol_pond_tank += (math.pi * ((d_pond / 2)**2) * t_pond) + (math.pi * ((d_tank / 2)**2) * max(0, tinggi_dinding - t_pond))
        
        # Volume Efektif Bundwall = Kapasitas * 110%
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
        
        # Safety Distances (using max tank diameter C15 ~ max_d_tank)
        shell_to_shell = (1/6 * max_d_tank + max([data[2] for data in tank_data][1] if len(tank_data)>1 else max_d_tank)) if max_d_tank <=45 else (1/3 * max_d_tank)
        if len(d_tanks) > 1:
            shell_to_shell = (1/6)*(max_d_tank + d_tanks[1]) if max(max_d_tank, d_tanks[1]) <=45 else (1/3)*(max_d_tank + d_tanks[1])
        else:
            shell_to_shell = 0 if max_d_tank ==0 else (1/6*max_d_tank if max_d_tank<=45 else 1/3*max_d_tank)
        
        tank_to_building = round(max(1.5, (1/6 if jenis_tank=="Floating Roof" else (1/6 if proteksi=="Proteksi" else 1/3)) * max_d_tank), 2)
        tank_to_property = round(max(1.5, (1/2 if jenis_tank=="Floating Roof" and proteksi=="Proteksi" else (1 if jenis_tank=="Floating Roof" else (1/2 if proteksi=="Proteksi" else 2))) * max_d_tank), 2)
        
        # Display Results
        st.markdown("---")
        st.header("📈 HASIL PERHITUNGAN")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Volume Bruto Bundwall (m³)", f"{volume_bruto:.2f}")
            st.metric("Volume Efektif Bundwall (m³)", f"{vol_efektif_bund:.2f}")
        with col_res2:
            st.metric("Volume Pondasi + Tank (m³)", f"{vol_pond_tank:.2f}")
            st.metric("Status", status)
        with col_res3:
            st.metric("Shell to Shell (m)", f"{shell_to_shell:.2f}")
            st.metric("Tank to Building (m)", f"{tank_to_building}")
            st.metric("Tank to Property (m)", f"{tank_to_property}")

elif shape == "Persegi":
    st.header("📏 Bundwall Persegi")
    
    # Input Bundwall Persegi
    col1, col2, col3 = st.columns(3)
    with col1:
        panjang = st.number_input("Panjang (m)", min_value=0.0, value=50.0, key="p_persegi")
    with col2:
        lebar = st.number_input("Lebar (m)", min_value=0.0, value=50.0, key="l_persegi")
    with col3:
        tinggi_dinding = st.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0, key="t_dinding_persegi")
    
    # Dimensi dinding bundwall persegi (lebar dinding dan tinggi? assuming lebar dinding)
    col4, col5 = st.columns(2)
    with col4:
        lebar_dinding_pjg = st.number_input("Lebar Dinding Panjang (m)", min_value=0.0, value=1.0, key="ld_pjg")
    with col5:
        lebar_dinding_lbr = st.number_input("Lebar Dinding Lebar (m)", min_value=0.0, value=1.0, key="ld_lbr")
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0, key="kap_tank_persegi")
    
    # Input data tangki dan pondasi sama seperti trapesium
    st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
    tank_data_persegi = []
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            with col_t1:
                d_pondasi = st.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0, key=f"d_pond{i}_per")
            with col_t2:
                t_pondasi = st.number_input(f"Tinggi Pondasi {i+1}
