import streamlit as st
import math

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
    .status-noncomply { color: #ff4b4b; font-
