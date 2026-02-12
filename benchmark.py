import streamlit as st
import subprocess
import time
import psutil
import pandas as pd
import os
import glob

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EcoCode AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (The Fix) ---
st.markdown("""
<style>
    /* Main Background - Deep Dark Grey */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Title Styling - Gradient Text */
    h1 {
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        text-align: center;
        padding-bottom: 0px;
    }
    
    /* Subtitle Styling */
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #b0b3b8;
        margin-bottom: 30px;
    }
    
    /* Metrics Styling - Big & Bright */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        color: #ffffff;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 16px;
        color: #a0a0a0;
    }
    
    /* BIG START BUTTON - Glowing Blue */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2193b0 0%, #6dd5ed 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
        font-size: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(33, 147, 176, 0.3);
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(33, 147, 176, 0.6);
    }
    
    /* Sidebar Status Badges */
    .status-badge {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: bold;
        text-align: center;
    }
    .status-ok { background-color: #1e3a2f; color: #4ade80; border: 1px solid #4ade80; }
    .status-warn { background-color: #3a2e1e; color: #facc15; border: 1px solid #facc15; }
    
</style>
""", unsafe_allow_html=True)

# --- 3. CONFIG & SETUP ---
TEST_SIZE = "500000000" 

# --- HEADER SECTION (Centered & Clean) ---
st.markdown("<h1>EcoCode AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>⚡ Algorithmic Energy Auditor & Green Code Optimizer</p>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Control Panel")

# System Check Badge
st.sidebar.markdown(f"""
<div class='status-badge' style='background-color: #262730; color: white; border: 1px solid #41444b;'>
    🖥️ System: {os.name.upper()}
</div>
""", unsafe_allow_html=True)

# Charger Check Badge
battery = psutil.sensors_battery()
if battery.power_plugged:
    st.sidebar.markdown("""
    <div class='status-badge status-warn'>
        ⚠️ CHARGER DETECTED<br><span style='font-size:0.8em'>Unplug for accuracy</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown(f"""
    <div class='status-badge status-ok'>
        ✅ ON BATTERY: {battery.percent}%
    </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("🔄 Refresh Status"):
    st.rerun()

# File Selection
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Select Algorithms")
cpp_files = glob.glob("*.cpp")
if not cpp_files:
    cpp_files = ["efficient.cpp", "inefficient.cpp"]

good_file = st.sidebar.selectbox("🌱 Efficient Code (Runs 1st)", cpp_files, index=min(1, len(cpp_files)-1))
bad_file = st.sidebar.selectbox("🔥 Inefficient Code (Runs 2nd)", cpp_files, index=0)

# --- HELPER FUNCTIONS ---
def compile_code(cpp_file):
    exe_name = cpp_file.replace(".cpp", "")
    if os.name == 'nt':
        exe_name += ".exe"
    os.system(f"g++ {cpp_file} -o {exe_name}")
    return exe_name

def run_stress_test(executable, chart_slot, status_slot, color_hex):
    start_batt = psutil.sensors_battery().percent
    start_time = time.time()
    cpu_data = []
    
    # 15s Test Duration
    while (time.time() - start_time) < 15:
        process = subprocess.Popen([f"./{executable}" if os.name != 'nt' else executable, TEST_SIZE])
        
        while process.poll() is None:
            current_cpu = psutil.cpu_percent(interval=0.1)
            
            # Update Status & Chart
            status_slot.markdown(f"**⚡ Status:** Measuring Energy... `Load: {current_cpu}%`")
            cpu_data.append(current_cpu)
            chart_slot.line_chart(cpu_data, height=220) 
            
            if (time.time() - start_time) > 15:
                process.terminate()
                break
        
    drop = start_batt - psutil.sensors_battery().percent
    avg_load = sum(cpu_data) / len(cpu_data) if cpu_data else 0
    return drop, avg_load

# --- MAIN INTERFACE ---

# 1. Warning Box (Cleaned up)
st.info("💡 **PRO TIP:** Close background apps (Chrome, Discord) for the most accurate energy reading.")

# 2. Start Button
if st.button("🚀 START ENERGY AUDIT"):
    
    # Error Check
    if good_file == bad_file:
        st.error("⛔ ERROR: You selected the same file twice. Please check sidebar.")
        st.stop()

    with st.spinner("⚙️ Compiling and calibrating sensors..."):
        good_exe = compile_code(good_file)
        bad_exe = compile_code(bad_file)
    
    st.divider()
    
    col1, col2 = st.columns(2)

    # --- LEFT: EFFICIENT ---
    with col1:
        st.markdown(f"### 🌱 Optimized: `{good_file}`")
        status_good = st.empty()
        chart_good = st.empty()
        drop_good, stress_good = run_stress_test(good_exe, chart_good, status_good, "#00FF00")
        st.success(f"Test Complete. Avg CPU Stress: {int(stress_good)}%")

    # --- RIGHT: INEFFICIENT ---
    with col2:
        st.markdown(f"### 🔥 Unoptimized: `{bad_file}`")
        status_bad = st.empty()
        chart_bad = st.empty()
        drop_bad, stress_bad = run_stress_test(bad_exe, chart_bad, status_bad, "#FF0000")
        st.error(f"Test Complete. Avg CPU Stress: {int(stress_bad)}%")

    # --- RESULTS DASHBOARD ---
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>🏆 Audit Report</h2>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Efficient Load", f"{int(stress_good)}%", delta="-Low Stress")
    m2.metric("Inefficient Load", f"{int(stress_bad)}%", delta="+High Stress", delta_color="inverse")
    m3.metric("Battery Saved", f"{drop_bad - drop_good}%", "Physical Drop")
    
    multiplier = stress_bad / stress_good if stress_good > 0 else 100
    m4.metric("Efficiency Gain", f"{multiplier:.1f}x", "Faster & Greener")

    # Final Recommendation Box
    if stress_good < stress_bad:
        st.balloons()
        st.markdown(f"""
        <div style="background-color: rgba(46, 125, 50, 0.2); padding: 20px; border-radius: 10px; border: 1px solid #4ade80; text-align: center;">
            <h3 style="color: #4ade80; margin:0;">✅ RECOMMENDATION: USE {good_file.upper()}</h3>
            <p style="color: #ffffff; margin-top: 10px;">
                The optimized algorithm reduces CPU power consumption by <b>{multiplier:.1f}x</b>. 
                Deploying this code reduces hardware thermal stress and extends battery life.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.caption("ℹ️ Verification: Double-check sidebar inputs if results appear identical.")