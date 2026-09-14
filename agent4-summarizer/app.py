import streamlit as st
import redis
import requests

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="SurgentAI Prototype", layout="wide")

# 2. Inject Custom CSS to mimic the prototype video's dark neon look
st.markdown("""
    <style>
    /* Dark background and neon green text for that medical/hacker vibe */
    .stApp {
        background-color: #070d19;
        color: #4af626;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3, h4, p, span, div {
        font-family: 'Courier New', Courier, monospace !important;
    }
    /* Style the text areas and buttons */
    .stTextArea textarea {
        background-color: #0b1426 !important;
        color: #4af626 !important;
        border: 1px solid #1f4068 !important;
    }
    .stButton>button {
        background-color: #0a4d68;
        color: white;
        border: 1px solid #4af626;
        width: 100%;
    }
    /* Hide default Streamlit header */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Connect to Redis
@st.cache_resource
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)

r = get_redis_client()

# --- TOP NAVIGATION BAR ---
st.markdown("### 🧬 SURGENTAI `OR-3` | `LIVE MEDICAL CENTER` | `EDGE-NODE ACTIVE` | `AIR-GAPPED`")
st.markdown("---")

# --- MAIN DASHBOARD GRID ---
col1, col2, col3 = st.columns([1, 1.2, 1])

# Left Column: Vision
with col1:
    st.markdown("#### AGENT 1 • VISION SENTINEL")
    st.info("📷 Live Video Feed: OFFLINE (Awaiting Agent 1)")
    st.markdown("**PROCEDURE CHECKLIST**")
    st.markdown("- [x] Trocar Insertion\n- [x] Pneumoperitoneum\n- [ ] Liver Retraction\n- [ ] Calot's Triangle Dissection")

# Middle Column: Vitals (Fake data to simulate the charts in your video)
with col2:
    st.markdown("#### AGENT 2 • VITALS PREDICTIVE ENGINE")
    st.line_chart({"BP_Sys": [120, 118, 119, 121, 115, 110, 105], "BP_Dia": [80, 79, 78, 80, 75, 72, 70]}, height=150)
    st.line_chart({"SpO2": [99, 99, 98, 98, 97, 95, 92]}, height=150)

# Right Column: Alerts & Status
with col3:
    st.markdown("#### ALERT LOG")
    st.error("🔴 CRITICAL: Vitals drop - Active dissection correlated.")
    st.warning("🟠 WARNING: SpO2 falling.")
    st.success("🟢 INFO: Intervention successful.")
    
    st.markdown("---")
    st.markdown("#### SYSTEM STATUS")
    st.markdown("* **Vision Engine:** ⏳ Pending\n* **Vitals Engine:** ⏳ Pending\n* **EMR Summarizer:** 🟢 ONLINE (TinyLlama)\n* **Network:** 🟢 AIR-GAPPED")

st.markdown("---")

# --- BOTTOM SECTION: AGENT 4 ---
col_report, col_btn = st.columns([4, 1])

with col_report:
    st.markdown("#### AGENT 4 • POST-OP EMR SUMMARIZER")
    report_area = st.empty()
    report_area.text_area("Final Clinical Report", value="Awaiting procedure completion...", height=200, disabled=True)

with col_btn:
    st.markdown("<br><br>", unsafe_allow_html=True) # Spacer
    if st.button("📄 Generate Report"):
        with st.spinner("Analyzing..."):
            transcript = "Incision made. Heart rate stable. Scalpel near critical vessel. Gallbladder extracted."
            prompt = f"Write a 3 sentence medical summary of these events: {transcript}"
            
            try:
                # Using TinyLlama as requested
                response = requests.post('http://localhost:11434/api/generate', json={
                    "model": "tinyllama:latest",
                    "prompt": prompt,
                    "stream": False
                })
                if response.status_code == 200:
                    report_area.text_area("Final Clinical Report", value=response.json()['response'], height=200)
                else:
                    st.error("Model error.")
            except Exception as e:
                st.error("Ollama is not running. Start it in terminal!")
