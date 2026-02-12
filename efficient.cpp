import streamlit as st
import subprocess
import time
import psutil
import pandas as pd
import os
import glob

# --- CONFIG ---
# 500 Million iterations to force the CPU to work hard
TEST_SIZE = "500000000" 

st.set_page_config(page_title="EcoCode AI", page_icon="📊", layout="wide")

st.title("📊 EcoCode AI: Efficiency Metrics")

# --- CHARGER CHECK ---
battery = psutil.sensors_battery()
col_msg, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("🔄 Refresh Power Status"):
        st.rerun()

with col_msg:
    if battery.power_plugged:
        st.warning("⚠️ CHARGER DETECTED! Unplug for accurate battery drop %.")
    else:
        st.success(f"✅ Running on Battery Power ({battery.percent}%)")

# --- SIDEBAR ---
st.sidebar.header("⚙️ Experiment Setup")
cpp_files = glob.glob("*.cpp")
if not cpp_files:
    cpp_files = ["inefficient.cpp", "efficient.cpp"]

# EFFICIENT RUNS FIRST (To set the standard)
good_file_cpp = st.sidebar.selectbox("Select Efficient Code (Runs 1st):", cpp_files, index=min(1, len(cpp_files)-1))
bad_file_cpp = st.sidebar.selectbox("Select Inefficient Code (Runs 2nd):", cpp_files, index=0)

# --- COMPILE ---
def compile_code(cpp_file):
    exe_name = cpp_file.replace(".cpp", "")
    if os.name == 'nt':
        exe_name += ".exe"
    os.system(f"g++ {cpp_file} -o {exe_name}")
    return exe_name

# --- ENGINE ---
def run_stress_test(executable, chart_slot, status_slot):
    start_batt = psutil.sensors_battery().percent
    start_time = time.time()
    cpu_data = []
    chart = chart_slot.line_chart([])
    
    # Run for 20 Seconds (Long enough to get data, short enough for video)
    while (time.time() - start_time) < 20:
        process = subprocess.Popen([f"./{executable}" if os.name != 'nt' else executable, TEST_SIZE])
        
        while process.poll() is None:
            current_cpu = psutil.cpu_percent(interval=0.1)
            current_time = round(time.time() - start_time, 1)
            
            new_row = pd.DataFrame({"CPU Load (%)": [current_cpu]}, index=[current_time])
            chart.add_rows(new_row)
            cpu_data.append(current_cpu)
            
            if (time.time() - start_time) > 20:
                process.terminate()
                break
        
        status_slot.text(f"Measuring CPU Cycles... {int(time.time() - start_time)}s / 20s")

    end_batt = psutil.sensors_battery().percent
    drop = start_batt - end_batt
    avg_load = sum(cpu_data) / len(cpu_data) if cpu_data else 0
    return drop, avg_load

# --- RUN BUTTON ---
if st.button("🚀 Analyze Performance Metrics"):
    
    with st.spinner(f"Compiling..."):
        good_exe = compile_code(good_file_cpp)
        bad_exe = compile_code(bad_file_cpp)

    col1, col2 = st.columns(2)

    # --- LEFT: EFFICIENT ---
    with col1:
        st.subheader(f"🌱 {good_file_cpp}")
        status_good = st.empty()
        chart_good = st.empty()
        drop_good, stress_good = run_stress_test(good_exe, chart_good, status_good)
        status_good.success(f"Analysis Complete")

    # --- RIGHT: INEFFICIENT ---
    with col2:
        st.subheader(f"🔥 {bad_file_cpp}")
        status_bad = st.empty()
        chart_bad = st.empty()
        drop_bad, stress_bad = run_stress_test(bad_exe, chart_bad, status_bad)
        status_bad.error(f"Analysis Complete")

    # --- THE NUMBERS ---
    st.markdown("---")
    st.subheader("🏆 Final Performance Report")
    
    c1, c2, c3 = st.columns(3)
    
    # 1. CPU Load Difference
    c1.metric("Average CPU Load", f"{int(stress_bad)}%", f"{int(stress_good)}% (Efficient)", delta_color="inverse")
    
    # 2. Battery Drop Difference
    c2.metric("Battery Drop", f"{drop_bad}%", f"{drop_good}% (Efficient)", delta_color="inverse")
    
    # 3. Efficiency Multiplier
    if stress_good > 0:
        multiplier = stress_bad / stress_good
        percentage_waste = ((stress_bad - stress_good) / stress_bad) * 100
    else:
        multiplier = 100 # Avoid divide by zero
        percentage_waste = 100

    c3.metric("Efficiency Score", f"{multiplier:.1f}x Better", f"{int(percentage_waste)}% Less Waste")

    # --- CONCLUSION BOX ---
    if stress_bad > stress_good:
        st.success(f"""
        ### ✅ Validated: {good_file_cpp} is {int(percentage_waste)}% more efficient.
        **The Data:** The inefficient code occupied **{int(stress_bad)}%** of the CPU's capacity, 
        while the optimized code used only **{int(stress_good)}%**. 
        Switching to the efficient algorithm reduces processor strain by a factor of **{multiplier:.1f}x**.
        """)