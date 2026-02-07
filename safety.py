import streamlit as st
import math

# Konfigurasi Halaman agar tampil penuh (wide)
st.set_page_config(page_title="BundSafe Tank Analytics", layout="wide")

# --- CUSTOM CSS UNTUK UI MODERN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .custom-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        position: relative;
    }

    /* Slice Biru di Pojok */
    .custom-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 12px;
        height: 50px;
        background: #007BFF;
        border-radius: 12px 0 12px 0;
    }

    /* Judul Tebal & Orbitron */
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem;
        font-weight: 900; /* Dibuat lebih tebal */
        color: #FFFFFF;
        margin-bottom: 20px;
        padding-left: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .status-comply {
        color: #00ff88;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    .status-noncomply {
        color: #ff4b4b;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.3rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='main-banner'>
    <h1 style='font-family: Orbitron; color: #00f2ff;'>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator | HSSE SULAWESI</p>
</div>
""", unsafe_allow_html=True)

col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

d_atas_pond, d_bawah_pond, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5, [0.0]*5

if shape == "Trapesium":
    st.markdown("<div class='custom-card'><div class='section-title'><b>BUNDWALL TRAPESIUM</b></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    panjang_luar = c1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar")
    lebar_luar = c2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar")
    tinggi_dinding = c3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'><div class='section-title'><b>DIMENSI DINDING</b></div>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    lebar_atas = c4.number_input("Lebar Atas (m)", min_value=0.0, key="lebar_atas")
    lebar_bawah = c5.number_input("Lebar Bawah (m)", min_value=0.0, key="lebar_bawah")
    kapasitas_tank_besar = c6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kapasitas")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='custom-card'><div class='section-title'><b>BUNDWALL PERSEGI</b></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    panjang = c1.number_input("Panjang (m)", min_value=0.0, key="p_per")
    lebar = c2.number_input("Lebar (m)", min_value=0.0, key="l_per")
    tinggi_dinding = c3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_per")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'><b>DIMENSI DINDING</b></div>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    lebar_dinding = c4.number_input("Lebar Dinding (m)", min_value=0.0, key="ld1_per")
    panjang_tebal_dinding = c5.number_input("Ketebalan Dinding (m)", min_value=0.0, key="ld2_per")
    kapasitas_tank_besar = c6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kap_per")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='custom-card'><div class='section-title'><b>DATA TANGKI & PONDASI (5 UNIT)</b></div>", unsafe_allow_html=True)
for i in range(5):
    with st.expander(f"Tangki {i+1}"):
        ct1, ct2, ct3, ct4 = st.columns(4)
        d_atas_pond[i] = ct1.number_input(f"D. Atas {i+1}", min_value=0.0, key=f"da_{i}")
        d_bawah_pond[i] = ct2.number_input(f"D. Bawah {i+1}", min_value=0.0, key=f"db_{i}")
        t_pondasis[i] = ct3.number_input(f"Tinggi P {i+1}", min_value=0.0, key=f"tp_{i}")
        d_tanks[i] = ct4.number_input(f"Diam. T {i+1}", min_value=0.0, key=f"dt_{i}")
st.markdown("</div>", unsafe_allow_html=True)

# Safety Distance dalam SATU GARIS
st.markdown("<div class='custom-card'><div class='section-title'><b>SAFETY DISTANCE</b></div>", unsafe_allow_html=True)
cs1, cs2, cs3, cs4 = st.columns(4)
d_safety_1 = cs1.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd1")
d_safety_2 = cs2.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd2")
proteksi = cs3.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="sd3")
jenis_tank = cs4.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="sd4")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("💾 HITUNG SEKARANG", type="primary", use_container_width=True):
    if shape == "Trapesium":
        t1_a = (panjang_luar - (2 * lebar_bawah))
        t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
        vol_bruto = (((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))) + (((lebar_bawah * ((lebar_bawah - lebar_atas) / 2)) / 2) * (panjang_luar - (((lebar_bawah - lebar_atas) / 2) + lebar_bawah)) * 2)
    else:
        vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal_dinding)

    vol_pond_tank = sum([( (1/3)*math.pi*t_pondasis[i]*( (d_atas_pond[i]/2)**2 + (d_bawah_pond[i]/2)**2 + ((d_atas_pond[i]/2)*(d_bawah_pond[i]/2)) ) ) + (math.pi*(d_tanks[i]/2)**2 * max(0, tinggi_dinding - t_pondasis[i])) for i in range(5)])
    vol_efektif_bund = vol_bruto - vol_pond_tank
    vol_min = kapasitas_tank_besar * 1.0
    
    # Perhitungan Safety
    max_d_s = max(d_safety_1, d_safety_2)
    shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
    f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
    tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
    tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else (1.0 if jenis_tank == "Floating Roof" else 2.0)) * d_safety_1), 2)

    is_comply = vol_efektif_bund > kapasitas_tank_besar * 1.1 and tinggi_dinding <= 1.8
    status_class = "status-comply" if is_comply else "status-noncomply"
    status_text = "✓ COMPLY - AMAN" if is_comply else "✗ NON COMPLY"

    st.markdown("<div class='custom-card'><div class='section-title'><b>📈 HASIL ANALISIS</b></div>", unsafe_allow_html=True)
    r1, r2, r3, r4, r5 = st.columns(5) # Dibuat satu garis lebih efisien
    r1.metric("Vol. Efektif", f"{vol_efektif_bund:.2f} m³")
    r2.metric("Vol. Min (100%)", f"{vol_min:.2f} m³")
    with r3:
        st.write("Status Safety:")
        st.markdown(f"<div class='{status_class}'>{status_text}</div>", unsafe_allow_html=True)
    r4.metric("Shell to Shell", f"{shell_to_shell:.2f} m")
    r5.metric("Tank to Property", f"{tank_to_property} m")
    st.markdown("</div>", unsafe_allow_html=True)
