import streamlit as st
import math

st.set_page_config(page_title="Calculator Safety Tangki Timbun", layout="wide")

st.markdown("""
<div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 15px; text-align: center; color: white; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>
    <h1 style='font-size: 2.5rem; margin: 0; font-weight: bold;'>🛢️ Calculator Safety Tangki Timbun</h1>
    <p style='font-size: 1.2rem; margin: 0.5rem 0; opacity: 0.95;'>Berdasarkan NFPA 30 "Flammable and Combustible Liquids Code"</p>
    <p style='font-size: 1.1rem; margin: 0; font-style: italic;'>Engineered By. Priyo</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

shape = st.selectbox("Pilih Bentuk Bundwall:", ["Trapesium", "Persegi"])

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
    tinggi_dinding = number_input_zero("
