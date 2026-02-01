import streamlit as st
import math

st.set_page_config(page_title="Calculator Safety Tangki Timbun", layout="wide")

# Banner dengan lambda bagus
st.markdown("""
<div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
    <h1 style='font-size: 2.5rem; margin: 0; font-weight: bold;'>🛢️ Calculator Safety Tangki Timbun</h1>
    <p style='font-size: 1.2rem; margin: 0.5rem 0; opacity: 0.95;'>Berdasarkan NFPA 30 "Flammable and Combustible Liquids Code"</p>
    <p style='font-size: 1.1rem; margin: 0; font-style: italic;'>Engineered By. Priyo</p>
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
            
            if vol_pond_tank < vol_efektif_bund:
                status = "✗ NON COMPLY - Volume bund kurang"
            elif tinggi_dinding > 1.8:
                status = "✗ NON COMPLY - Tinggi dinding > 1,8 m"
            else:
                status = "✓ COMPLY - AMAN" if vol_pond_tank >= vol_efektif_bund else "CHECK DATA"
            
            c15 = d_tanks[0]
            c19 = d_tanks[1] if len(d_tanks)>1 else c15
            shell_to_shell = (1/6)*(c15 + c19) if max(c15, c19) <= 45 else (1/3)*(c15 + c19)
            
            factor_build = 1/6 if jenis_tank == "Floating Roof" else (1/6 if proteksi == "Proteksi" else 1/3)
            tank_to_building = round(max(1.5, factor_build * c15), 2)
            
            factor_prop = 0.5 if (jenis_tank == "Floating Roof" and proteksi == "Proteksi") else \
                          1 if jenis_tank == "Floating Roof" else (0.5 if proteksi == "Proteksi" els




