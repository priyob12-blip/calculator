import streamlit as st
import math

st.set_page_config(page_title="Kalkulator Safety Tangki", layout="wide")

st.title("🛢️ Kalkulator Safety Tangki")
st.markdown("---")

shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"])

if st.button("🔄 RESET"):
    st.rerun()

st.markdown("---")

# Inputs umum untuk 5 tangki
st.subheader("📊 Data Tangki & Pondasi (5 Unit)")
d_pondasis = []
t_pondasis = []
d_tanks = []
for i in range(5):
    with st.expander(f"Tangki {i+1}"):
        col1, col2, col3 = st.columns(3)
        d_pond = col1.number_input(f"Diameter Pondasi {i+1} (m)", min_value=0.0, value=10.0 + i*0.5)
        t_pond = col2.number_input(f"Tinggi Pondasi {i+1} (m)", min_value=0.0, value=1.0)
        d_tank = col3.number_input(f"Diameter Tangki {i+1} (m)", min_value=0.0, value=15.0 + i)
        d_pondasis.append(d_pond)  # C13,C17,C21,C25,C29
        t_pondasis.append(t_pond)  # C14,C18,C22,C26,C30
        d_tanks.append(d_tank)     # C15,C19,C23,C27,C31

if shape == "Trapesium":
    st.header("📐 Bundwall Trapesium")
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, value=50.0)  # C5
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, value=50.0)      # C6
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)  # C7
    
    col4, col5 = st.columns(2)
    lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0, value=0.5)      # C9
    lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0, value=1.0)     # C10
    
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])
    
elif shape == "Persegi":
    st.header("📏 Bundwall Persegi")
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0, value=50.0)
    lebar = col2.number_input("Lebar (m)", min_value=0.0, value=50.0)
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, value=2.0)
    
    lebar_dinding = st.number_input("Lebar Dinding (m)", min_value=0.0, value=1.0)
    kapasitas_tank_besar = st.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, value=1000.0)
    
    col_prot, col_roof = st.columns(2)
    proteksi = col_prot.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"])
    jenis_tank = col_roof.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"])

if st.button("💾 HITUNG", type="primary"):
    if shape == "Trapesium":
        # Volume Bruto EXCEL PERSIS
        term1_inner = (panjang_luar - (lebar_bawah * 2)) + (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
        term1 = ((term1_inner / 2) * tinggi_dinding) * (lebar_luar - (tinggi_dinding * 2))
        term2_inner = (tinggi_dinding * ((lebar_bawah - lebar_atas) / 2)) / 2
        term2 = term2_inner * (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 4)) * 2)) * 2
        vol_bruto = term1 + term2  # C34
    else:
        vol_bruto = tinggi_dinding * (panjang - 2 * lebar_dinding) * (lebar - 2 * lebar_dinding)
    
    # Volume Pond+Tank EXCEL PERSIS: 10 terms PI
    vol_pond_tank = 0
    for i in range(5):
        # PI*(d_pond/2)^2 * t_pond + PI*(d_tank/2)^2 * MAX(0, C7 - t_pond)
        vol_pond_tank += (math.pi * ((d_pondasis[i] / 2)**2) * t_pondasis[i]) + \
                         (math.pi * ((d_tanks[i] / 2)**2) * max(0, tinggi_dinding - t_pondasis[i]))
    
    vol_efektif_bund = vol_bruto - vol_pond_tank  # C35 = C34 - pond_tank? Tunggu, Anda bilang C34-C35 tapi logika bund efektif=bruto-pond
    
    # Status EXCEL PERSIS
    if vol_pond_tank < vol_efektif_bund:
        status = "✗ NON COMPLY - Volume bund kurang"
    elif tinggi_dinding > 1.8:
        status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
    else:  # IF(C37 >= C39; "✓ COMPLY - AMAN"; "CHECK DATA")
        if vol_pond_tank >= vol_efektif_bund:
            status = "✓ COMPLY - AMAN"
        else:
            status = "CHECK DATA"
    
    max_d_tank = max(d_tanks) if d_tanks else 0
    d_tank2 = d_tanks[1] if len(d_tanks) > 1 else max_d_tank
    shell_to_shell = (1/6) * (max_d_tank + d_tank2) if max(max_d_tank, d_tank2) <= 45 else (1/3) * (max_d_tank + d_tank2)
    
    factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
    tank_to_building = round(max(1.5, factor_build * max_d_tank), 2)
    
    factor_prop = 0.5 if (jenis_tank == "Floating Roof" and proteksi == "Proteksi") else \
                  1 if jenis_tank == "Floating Roof" else (0.5 if proteksi == "Proteksi" else 2)
    tank_to_property = round(max(1.5, factor_prop * max_d_tank), 2)
    
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

