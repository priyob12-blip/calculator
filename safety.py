import streamlit as st
import math
from fpdf import FPDF
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="BundSafe Tank Analytics", 
    page_icon="⚡", 
    layout="wide"
)

# --- CUSTOM CSS UNTUK UI MODERN & DESIGN KOTAK ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
    
    .main-banner {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
        url('https://images.unsplash.com/photo-1516937941344-00b4e0337589?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; padding: 4rem 2rem;
        border-radius: 20px; text-align: center; color: white; margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);
    }
    .main-banner h1 { font-family: 'Orbitron', sans-serif; font-size: 3.5rem; color: #00f2ff; text-shadow: 0 0 15px rgba(0, 242, 255, 0.6); }
    .custom-card {
        background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px; padding: 20px; margin-bottom: 25px; position: relative; overflow: hidden;
    }
    .custom-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 10px; height: 40px;
        background: #007BFF; border-radius: 0 0 10px 0;
    }
    .section-title { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 800; color: #000000; margin-bottom: 20px; padding-left: 15px; }
    .status-comply { color: #00ff88; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
    .status-noncomply { color: #ff4b4b; font-family: 'Orbitron', sans-serif; font-size: 1.2rem; font-weight: bold; }
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

# --- CLASS PDF GENERATOR (TEMPLATE COMPACT 1 HALAMAN) ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, 'Laporan Analisis Bundwall (BundSafe)', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.set_text_color(100, 100, 100)
        # HANYA TANGGAL
        self.cell(0, 5, f'Tanggal Cetak: {datetime.now().strftime("%d %B %Y")}', 0, 1, 'C')
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(10, 25, 200, 25)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(240, 240, 240) # Abu-abu muda
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, f'  {label}', 0, 1, 'L', 1)
        self.ln(1)

    def add_row_compact(self, label, value):
        self.set_font('Arial', '', 9)
        self.cell(70, 5, label, 0)
        self.set_font('Arial', 'B', 9)
        self.cell(0, 5, f": {value}", 0, 1)

# --- FUNGSI PEMBANTU SAFETY DISTANCE ---
def estimate_cap(dia):
    # Mapping Diameter ke Kapasitas sesuai Tabel 4
    if dia <= 6.68: return 150
    elif dia <= 7.64: return 200
    elif dia <= 8.59: return 250
    elif dia <= 9.55: return 500
    elif dia <= 11.46: return 700
    elif dia <= 13.37: return 1500
    elif dia <= 15.28: return 2000
    elif dia <= 17.19: return 2500
    elif dia <= 19.10: return 5000
    elif dia <= 27.69: return 10000
    elif dia <= 30.56: return 12500
    elif dia <= 33.42: return 15000
    elif dia <= 40.11: return 20000
    elif dia <= 43.93: return 25000
    elif dia <= 48.70: return 30000
    else: return 50000

def get_nfpa_dist(cap):
    # Logika TUNGGAL untuk Kelas I, II, dan IIIA (Pertalite, Pertamax, Solar, MFO)
    if cap <= 1.045: return 1.5, 1.5
    elif cap <= 2.85: return 3.0, 1.5
    elif cap <= 45.6: return 4.5, 1.5
    elif cap <= 114.0: return 6.0, 1.5
    elif cap <= 190.0: return 9.0, 3.0
    elif cap <= 380.0: return 15.0, 4.5
    elif cap <= 1900.0: return 24.0, 7.5
    elif cap <= 3800.0: return 30.0, 10.5
    elif cap <= 7600.0: return 40.5, 13.5
    elif cap <= 11400.0: return 49.5, 16.5
    else: return 52.5, 18.0

# --- BAGIAN INPUT UTAMA ---
col_shape, col_reset = st.columns([4, 1])
with col_shape:
    shape = st.selectbox("Pilih Jenis Bundwall:", ["Trapesium", "Persegi"], key="shape_select")
with col_reset:
    if st.button("🔄 RESET SYSTEM", use_container_width=True):
        st.rerun()

d_atas_pond, d_bawah_pond, t_pondasis, d_tanks = [0.0]*5, [0.0]*5, [0.0]*5, [0.0]*5

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
    cs1, cs2, cs3 = st.columns(3)
    produk = cs1.selectbox("Jenis BBM:", ["Pertalite", "Pertamax", "Solar", "Avtur", "MFO"], key="prod_tr")
    d_safety_1 = cs2.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_tr")
    d_safety_2 = cs3.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_tr")
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
    cs1, cs2, cs3 = st.columns(3)
    produk = cs1.selectbox("Jenis BBM:", ["Pertalite", "Pertamax", "Solar", "Avtur", "MFO"], key="prod_per")
    d_safety_1 = cs2.number_input("D. Tangki 1 (m)", min_value=0.0, key="sd_d1_pr")
    d_safety_2 = cs3.number_input("D. Tangki 2 (m)", min_value=0.0, key="sd_d2_pr")
    st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIKA PERHITUNGAN & OUTPUT ---
if st.button("💾 HITUNG SEKARANG", type="primary", use_container_width=True):
    # --- RUMUS ASLI (KOMPLEKS) UNTUK VOLUME BRUTO ---
    if shape == "Trapesium":
        t1_a = (panjang_luar - (2 * lebar_bawah))
        t1_b = (panjang_luar - ((lebar_atas + ((lebar_bawah - lebar_atas) / 2)) * 2))
        term1 = ((t1_a + t1_b) / 2 * tinggi_dinding) * (lebar_luar - (2 * lebar_bawah))
        s_val = (lebar_bawah - lebar_atas) / 2
        term2 = ((lebar_bawah * s_val) / 2) * (panjang_luar - (s_val + lebar_bawah)) * 2
        vol_bruto = term1 + term2
    else:
        vol_bruto = tinggi_dinding * (panjang - 2*lebar_dinding) * (lebar - 2*panjang_tebal_dinding)

    vol_pond_tank = 0
    # PERBAIKAN SYNTAX LOOP DI SINI:
    for i in range(5):
        r_atas, r_bawah = d_atas_pond[i] / 2, d_bawah_pond[i] / 2
        v_pondasi = (1/3) * math.pi * t_pondasis[i] * (r_atas**2 + r_bawah**2 + (r_atas * r_bawah))
        v_tank = math.pi * (d_tanks[i]/2)**2 * max(0, tinggi_dinding - t_pondasis[i])
        vol_pond_tank += (v_pondasi + v_tank)
    
    vol_efektif_bund = vol_bruto - vol_pond_tank
    vol_min = kapasitas_tank_besar * 1.0

    # --- LOGIKA SAFETY DISTANCE SEDERHANA ---
    est_kapasitas = estimate_cap(d_safety_1)
    dist_fac, dist_road = get_nfpa_dist(est_kapasitas) 
    
    max_d_s = max(d_safety_1, d_safety_2)
    shell_to_shell = (1/6)*(d_safety_1 + d_safety_2) if max_d_s <= 45 else (1/3)*(d_safety_1 + d_safety_2)
    
    tank_to_road = dist_road 
    tank_to_prop = dist_fac  

    is_comply = vol_efektif_bund > kapasitas_tank_besar * 1 and tinggi_dinding <= 1.8
    status_class = "status-comply" if is_comply else "status-noncomply"
    status_text = "COMPLY - AMAN" if is_comply else "NON COMPLY"
    status_symbol = "✓" if is_comply else "✗"

    st.markdown(f"### 📈 HASIL ANALISIS")
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Volume Bruto", f"{vol_bruto:.2f} m³")
    res1.metric("Vol. Pond+Tank", f"{vol_pond_tank:.2f} m³")
    res2.metric("Vol. Efektif Bund", f"{vol_efektif_bund:.2f} m³")
    res2.metric("Volume Minimum", f"{vol_min:.2f} m³")
    with res3:
        st.write("Status Safety:")
        st.markdown(f"<div class='{status_class}'>{status_symbol} {status_text}</div>", unsafe_allow_html=True)
    
    # Klasifikasi Teks
    if produk in ["Pertalite", "Pertamax"]:
        kelas_bbm = "Class I"
    elif produk == "Solar":
        kelas_bbm = "Class II"
    else: # MFO, Avtur
        kelas_bbm = "Class IIIA"

    if d_safety_1 > 0:
        st.markdown("---")
        st.write(f"**Safety Distance Minimum (NFPA 30 - {produk}):**")
        sd_col1, sd_col2, sd_col3 = st.columns(3)
        sd_col1.metric("Shell to Shell", f"{shell_to_shell:.2f} m")
        sd_col2.metric("Shell to Building", f"{tank_to_road} m") 
        sd_col3.metric("Shell to Property", f"{tank_to_prop} m") 
        
        caption_text = f"Estimasi Kapasitas: {est_kapasitas} KL. Klasifikasi: {kelas_bbm} (Tabel Utama NFPA 30)."
        st.caption(caption_text)

    # --- FITUR REKOMENDASI & PREPARE PDF DATA ---
    rec_text_fisik = []
    rec_text_admin = []
    
    if not is_comply:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 LIHAT REKOMENDASI "):
            st.markdown("### Rekomendasi Teknis HSSE")
            kekurangan = vol_min - vol_efektif_bund
            
            rec_col1, rec_col2 = st.columns(2)
            
            with rec_col1:
                st.info("**Opsi Rekayasa Fisik**")
                luas_estimasi = vol_bruto / tinggi_dinding if tinggi_dinding > 0 else 1
                tambah_h = kekurangan / luas_estimasi
                target_h = tinggi_dinding + tambah_h
                
                if target_h <= 1.8:
                    msg_1 = f"1. **Peninggian Dinding:** Target baru: **{target_h:.2f} m**."
                    st.write(msg_1)
                    rec_text_fisik.append(msg_1.replace("**",""))
                else:
                    msg_1 = f"1. **Perluasan Area:** Peninggian dinding > 1.8m tidak disarankan."
                    st.write(msg_1)
                    rec_text_fisik.append(msg_1.replace("**",""))
                
                msg_2 = "2. **Remote Impounding:** Gunakan saluran peluap ke kolam sekunder."
                st.write(msg_2)
                rec_text_fisik.append(msg_2.replace("**",""))

            with rec_col2:
                st.info("**Opsi Administratif**")
                aman_kl = vol_efektif_bund / 1.0
                msg_3 = f"1. **Downgrading:** Batasi isi tangki max **{vol_efektif_bund:.2f} KL**."
                st.write(msg_3)
                rec_text_admin.append(msg_3.replace("**",""))
                
                msg_4 = "2. **Adjustment HLA:** Atur ulang sensor High Level Alarm."
                st.write(msg_4)
                rec_text_admin.append(msg_4.replace("**",""))
                
            st.warning("⚠️ Perubahan fisik wajib melalui kajian teknis.")

    # --- GENERATE PDF REPORT (COMPACT 1 PAGE) ---
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. Info Data
    pdf.chapter_title('1. Data Input')
    dimensi_str = f"P: {panjang_luar}m, L: {lebar_luar}m, T: {tinggi_dinding}m" if shape == 'Trapesium' else f"P: {panjang}m, L: {lebar}m, T: {tinggi_dinding}m"
    pdf.add_row_compact('Jenis Bundwall', shape)
    pdf.add_row_compact('Produk', f"{produk} ({kelas_bbm})")
    pdf.add_row_compact('Kapasitas Max', f"{kapasitas_tank_besar} KL")
    pdf.add_row_compact('Dimensi', dimensi_str)
    pdf.ln(2)

    # 2. Hasil Perhitungan
    pdf.chapter_title('2. Hasil Analisis Kapasitas')
    pdf.add_row_compact('Volume Bruto', f'{vol_bruto:.2f} m3')
    pdf.add_row_compact('Vol. Pondasi+Tank', f'{vol_pond_tank:.2f} m3')
    pdf.add_row_compact('Volume Efektif', f'{vol_efektif_bund:.2f} m3')
    pdf.add_row_compact('Volume Minimum', f'{vol_min:.2f} m3')
    
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 10)
    if is_comply:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 6, f'STATUS: {status_text}', 0, 1)
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 6, f'STATUS: {status_text}', 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # 3. Safety Distance
    pdf.chapter_title('3. Analisis Safety Distance (NFPA 30)')
    pdf.add_row_compact('Klasifikasi', f'{kelas_bbm}')
    pdf.add_row_compact('Est. Kapasitas', f'{est_kapasitas} KL')
    pdf.add_row_compact('Shell to Shell', f'{shell_to_shell:.2f} m')
    pdf.add_row_compact('Shell to Building', f'{tank_to_road} m')
    pdf.add_row_compact('Shell to Property', f'{tank_to_prop} m')
    pdf.ln(2)

    # 4. Rekomendasi (Compact)
    if not is_comply:
        pdf.chapter_title('4. Rekomendasi Perbaikan')
        pdf.set_font('Arial', '', 9)
        
        if rec_text_fisik:
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(0, 5, 'Fisik:', 0, 1)
            pdf.set_font('Arial', '', 9)
            for item in rec_text_fisik:
                safe_item = item.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 5, f"- {safe_item}")
            
        if rec_text_admin:
            pdf.ln(1)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(0, 5, 'Administratif:', 0, 1)
            pdf.set_font('Arial', '', 9)
            for item in rec_text_admin:
                safe_item = item.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 5, f"- {safe_item}")
        
        pdf.ln(3)
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(100, 0, 0)
        pdf.multi_cell(0, 4, "Catatan: Perubahan fisik wajib melalui kajian teknis sipil.")

    # Output Button (Safe Encoding)
    pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
    
    st.download_button(
        label="📄 DOWNLOAD LAPORAN PDF",
        data=pdf_bytes,
        file_name=f"Laporan_BundSafe_{datetime.now().strftime
