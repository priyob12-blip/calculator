import streamlit as st
import math

# --- KONFIGURASI HALAMAN ---
# Mengganti favicon menjadi logo custom "Shield Tank HSSE" yang lebih modern
st.set_page_config(
    page_title="BundSafe Tank Analytics", 
    page_icon="https://raw.githubusercontent.com/Arindama/BundSafe/main/logo_shield_tank.png", 
    layout="wide"
)

# --- CUSTOM CSS UNTUK UI MODERN & DESIGN KOTAK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    /* Banner Utama */
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-banner h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem;
        color: #00f2ff;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }

    /* Card Section dengan Slice Biru */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .custom-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 10px;
        height: 40px;
        background: #007BFF;
        border-radius: 0 0 10px 0;
    }

    /* JUDUL HITAM & BOLD */
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #000000; 
        margin-bottom: 20px;
        padding-left: 15px;
    }

    /* Status Label Styling */
    .status-comply {
        color: #00ff88;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    .status-noncomply {
        color: #ff4b4b;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- IMPLEMENTASI BANNER ---
st.markdown("""
<div class='main-banner'>
    <h1>BundSafe Tank Analytics</h1>
    <p>Bundwall & Storage Tank Safety Calculator</p>
    <div style='text-align: center; margin-top: 10px;'>
        <span style='background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; border-radius: 5px;'>Standardized by NFPA 30 | HSSE SULAWESI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

def number_input_zero(label, key):
    return st.number_input(label, min_value=0.0, value=0.0, key=key)

# Persiapan List Data Tangki
d_atas_pond, d_bawah_pond, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5, [0.0]*5

# UI Logic berdasarkan Shape
if shape == "Trapesium":
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Trapesium</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang_luar = col1.number_input("Panjang Luar (m)", min_value=0.0, key="p_luar")
    lebar_luar = col2.number_input("Lebar Luar (m)", min_value=0.0, key="l_luar")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_dinding")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    lebar_atas = col4.number_input("Lebar Atas (m)", min_value=0.0, key="lebar_atas")
    lebar_bawah = col5.number_input("Lebar Bawah (m)", min_value=0.0, key="lebar_bawah")
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kapasitas")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            ct1, ct2, ct3, ct4 = st.columns(4)
            d_atas_pond[i] = ct1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_tr_{i}")
            d_bawah_pond[i] = ct2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_tr_{i}")
            t_pondasis[i] = ct3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_tr_{i}")
            d_tanks[i] = ct4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_tr_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
    cs1, cs2, cs3, cs4 = st.columns(4)
    d_safety_1 = cs1.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_tr")
    d_safety_2 = cs2.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_tr")
    proteksi = cs3.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_tr")
    jenis_tank = cs4.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_tr")
    st.markdown("</div>", unsafe_allow_html=True)

else:  # Persegi
    st.markdown("<div class='custom-card'><div class='section-title'>Bundwall Persegi</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    panjang = col1.number_input("Panjang (m)", min_value=0.0, key="p_per")
    lebar = col2.number_input("Lebar (m)", min_value=0.0, key="l_per")
    tinggi_dinding = col3.number_input("Tinggi Dinding (m)", min_value=0.0, key="t_per")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Dimensi Dinding</div>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    lebar_dinding = col4.number_input("Lebar Dinding (m)", min_value=0.0, key="ld1_per")
    panjang_tebal_dinding = col5.number_input("Ketebalan Dinding (m)", min_value=0.0, key="ld2_per")
    kapasitas_tank_besar = col6.number_input("Kapasitas Tangki Terbesar (KL)", min_value=0.0, key="kap_per")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Data Tangki & Pondasi (5 Unit)</div>", unsafe_allow_html=True)
    for i in range(5):
        with st.expander(f"Tangki {i+1}"):
            cp1, cp2, cp3, cp4 = st.columns(4)
            d_atas_pond[i] = cp1.number_input(f"D. Atas Pondasi {i+1}", min_value=0.0, key=f"d_at_pr_{i}")
            d_bawah_pond[i] = cp2.number_input(f"D. Bawah Pondasi {i+1}", min_value=0.0, key=f"d_bw_pr_{i}")
            t_pondasis[i] = cp3.number_input(f"Tinggi Pondasi {i+1}", min_value=0.0, key=f"t_pd_pr_{i}")
            d_tanks[i] = cp4.number_input(f"Diameter Tangki {i+1}", min_value=0.0, key=f"d_tk_pr_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='custom-card'><div class='section-title'>Safety Distance</div>", unsafe_allow_html=True)
    cs1, cs2, cs3, cs4 = st.columns(4)
    d_safety_1 = cs1.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_pr")
    d_safety_2 = cs2.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_pr")
    proteksi = cs3.selectbox("Proteksi:", ["Proteksi", "Non Proteksi"], key="prot_per_sd")
    jenis_tank = cs4.selectbox("Jenis Tangki:", ["Fixed Roof", "Floating Roof"], key="jenis_per_sd")
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIKA PERHITUNGAN & OUTPUT ---
if st.button("💾 HITUNG SEKARANG", type="primary", use_container_width=True):
    # Kalkulasi Volume Bruto
    if shape == "Trapesium":
        t1_a = (panjang_luar - (2 * lebar_bawah))
        t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
        term1 = ((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))
        s_val = (lebar_bawah - lebar_atas) / 2
        term2 = ((lebar_bawah * s_val) / 2) * (panjang_luar - (s_val + lebar_bawah)) * 2
        vol_bruto = term1 + term2
    else:
        vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal_dinding)

    # Displacement (Dihitung 5 unit seperti di input sebelumnya)
    vol_pond_tank = 0
    for i in range(5):
        r_atas, r_bawah = d_atas_pond[i] / 2, d_bawah_pond[i] / 2
        v_pondasi = (1/3) * math.pi * t_pondasis[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
        v_tank = math.pi * (d_tanks[i]/2)**2 * max(0, tinggi_dinding - t_pondasis[i])
        vol_pond_tank += (v_pondasi + v_tank)
    
    vol_efektif_bund = vol_bruto - vol_pond_tank
    vol_min = kapasitas_tank_besar * 1.0
    
    # Hitung Safety Distance
    max_d_s = max(d_safety_1, d_safety_2)
    shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
    f_build = 1/6 if (jenis_tank == "Floating Roof" or proteksi == "Proteksi") else 1/3
    tank_to_build = round(max(1.5, f_build * d_safety_1), 2)
    tank_to_property = round(max(1.5, (0.5 if proteksi == "Proteksi" else (1.0 if jenis_tank == "Floating Roof" else 2.0)) * d_safety_1), 2)

    is_comply = vol_efektif_bund > kapasitas_tank_besar * 1 and tinggi_dinding <= 1.8
    status_class = "status-comply" if is_comply else "status-noncomply"
    status_text = "✓ COMPLY - AMAN" if is_comply else "✗ NON COMPLY"

    st.markdown(f"### 📈 HASIL ANALISIS")
    
    # Baris 1: Metrik Volume
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Volume Bruto", f"{vol_bruto:.2f} m³")
    res1.metric("Vol. Pond+Tank", f"{vol_pond_tank:.2f} m³")
    res2.metric("Vol. Efektif Bund", f"{vol_efektif_bund:.2f} m³")
    res2.metric("Volume Minimum", f"{vol_min:.2f} m³")
    
    with res3:
        st.write("Status Safety:")
        st.markdown(f"<div class='{status_class}'>{status_text}</div>", unsafe_allow_html=True)
    
    # Baris 2: Safety Distance (HANYA TAMPIL JIKA d_safety_1 > 0)
    if d_safety_1 > 0:
        st.markdown("---")
        st.write("**Safety Distance Minimum :**")
        sd_col1, sd_col2, sd_col3 = st.columns(3)
        sd_col1.metric("Shell to Shell", f"{shell_to_shell:.2f} m")
        sd_col2.metric("Tank to Building", f"{tank_to_build} m")
        sd_col3.metric("Tank to Property", f"{tank_to_property} m")

    # --- FITUR REKOMENDASI (HIDE-SLIDE) ---
    if not is_comply:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 LIHAT REKOMENDASI "):
            st.markdown("### Rekomendasi Teknis HSSE")
            
            kekurangan = vol_min - vol_efektif_bund
            
            rec_col1, rec_col2 = st.columns(2)
            
            with rec_col1:
                st.info("**Opsi Rekayasa Fisik**")
                # Simulasi sederhana tambahan tinggi
                luas_estimasi = vol_bruto / tinggi_dinding if tinggi_dinding > 0 else 1
                tambah_h = kekurangan / luas_estimasi
                target_h = tinggi_dinding + tambah_h
                
                if target_h <= 1.8:
                    st.write(f"1. **Peninggian Dinding:** Target tinggi dinding baru adalah **{target_h:.2f} m** (Sesuai batas NFPA < 1.8m).")
                else:
                    st.write(f"1. **Perluasan Area:** Peninggian dinding hingga 1.8m tidak cukup. Diperlukan perluasan panjang/lebar area.")
                
                st.write("2. **Remote Impounding:** Integrasikan antar bundwall untuk atasi keterbatasan volume. Gunakan sistem Remote Impounding dengan saluran peluap ke kolam sekunder")

            with rec_col2:
                st.info("**Opsi Administratif & Operasional**")
                aman_kl = vol_efektif_bund / 1.0
                st.write(f"1. **Downgrading Kapasitas:** Batasi pengisian tangki terbesar maksimal hingga **{aman_kl:.2f} KL**.")
                st.write("2. **Adjustment HLA:** Atur ulang sensor *High Level Alarm* (HLA) sesuai kapasitas bundwall saat ini.")
                
            st.warning("⚠️ Perubahan fisik wajib melalui kajian teknis sipil dan pemastian jarak aman (Safety Distance) tetap terjaga.")
