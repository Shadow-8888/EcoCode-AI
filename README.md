# 🌱 EcoCode AI: Automated Energy Efficiency Auditor

### 🏆 Infomatrix Asia 2026 Submission
**Category:** AI Programming  
**Team:** Idea to Algorithm (I2A)  
**Project Status:** 🟢 Completed Prototype

---

![EcoCode AI Dashboard](dashboard.png)
*(Screenshot of EcoCode AI analyzing algorithmic energy consumption in real-time)*

## 🌍 The Problem
Software inefficiency is a silent contributor to global energy consumption. Mobile apps running unoptimized code (e.g., $O(n^2)$ sorting algorithms) drain batteries faster, leading to:
1.  **Reduced Battery Life** for users.
2.  **Device Overheating** and hardware degradation.
3.  **Increased Carbon Footprint** due to wasted electricity.

## 💡 The Solution
**EcoCode AI** is a benchmarking tool that acts as an "Energy Detective" for software. It allows developers to:
* **Simulate** heavy computational tasks using C++ algorithms.
* **Measure** real-time CPU power consumption and physical battery discharge rates.
* **Compare** efficient vs. inefficient code side-by-side.
* **Visualize** the environmental impact of their code choices.

## ✨ Key Features
* **🔋 Real-Time Battery Stress Test:** Monitors physical battery percentage drop during code execution.
* **cpu CPU Load Analysis:** Tracks processor usage spikes to identify inefficient loops.
* **📊 Comparative Dashboard:** Side-by-side visualization of "Efficient" (Green) vs. "Inefficient" (Red) algorithms.
* **🤖 AI Recommendation Engine:** Automatically calculates an "Efficiency Score" (e.g., "12x Better") and suggests optimizations.

## 🛠️ Technology Stack
* **Frontend:** Streamlit (Python) for the interactive dashboard.
* **Backend Logic:** Python (`psutil`, `subprocess`) for hardware sensor bridging.
* **Test Algorithms:** C++ (`g++` Compiler) for high-performance simulation.
* **Data Processing:** Pandas for real-time charting and metrics.

## 🚀 How to Run Locally

### Prerequisites
* Python 3.8+
* G++ Compiler (MinGW for Windows or standard Linux/Mac compilers)

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Shadow-8888/EcoCode-AI.git](https://github.com/Shadow-8888/EcoCode-AI.git)
    cd EcoCode-AI
    ```

2.  **Install Dependencies:**
    ```bash
    pip install streamlit psutil pandas
    ```

3.  **Run the Tool:**
    ```bash
    streamlit run benchmark.py
    ```

4.  **Usage:**
    * Unplug your laptop charger (for accurate battery readings).
    * Select the Efficient (`efficient.cpp`) and Inefficient (`inefficient.cpp`) files from the sidebar.
    * Click **"🚀 Start Live Test"**.

## 📉 Results & Impact
During testing, EcoCode AI demonstrated that replacing an inefficient summation loop with a mathematical formula resulted in:
* **92% Reduction** in CPU Load.
* **Zero Battery Drop** (vs. 1% drop for the inefficient code).
* **15x Improvement** in Efficiency Score.

## 📜 License
This project is open-source and available under the MIT License.

---
*Built with ❤️ for a greener digital future.*
