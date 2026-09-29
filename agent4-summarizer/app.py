import streamlit as st
import redis
import json
import time
import requests

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="SurgentAI Prototype", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #070d19; color: #4af626; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3, h4, p, span, div { font-family: 'Courier New', Courier, monospace !important; }
    .stTextArea textarea { background-color: #0b1426 !important; color: #4af626 !important; border: 1px solid #1f4068 !important; }
    .stButton>button { background-color: #0a4d68; color: white; border: 1px solid #4af626; width: 100%; }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Redis Connection (The Bridge to Agent 1)
@st.cache_resource
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)

r = get_redis_client()

# Subscribe to the channel Agent 1 is publishing to
if "pubsub" not in st.session_state:
    st.session_state.pubsub = r.pubsub()
    st.session_state.pubsub.subscribe("surgery_stream")

# 3. Initialize Memory (Session State)
if "tools" not in st.session_state: st.session_state.tools = "Awaiting Vision Data..."
if "transcript" not in st.session_state: st.session_state.transcript = []

# (Baseline arrays for Agent 2 vitals charts - these will remain flat until Agent 2 is built)
if "bp_sys" not in st.session_state: st.session_state.bp_sys = [120] * 20
if "bp_dia" not in st.session_state: st.session_state.bp_dia = [80] * 20
if "spo2" not in st.session_state: st.session_state.spo2 = [99] * 20
if "alerts" not in st.session_state: st.session_state.alerts = []

# --- UI LAYOUT ---
st.markdown("### 🧬 SURGENTAI `OR-3` | `LIVE MEDICAL CENTER` | `EDGE-NODE ACTIVE`")
st.markdown("---")

# The master switch to start the Redis event loop
live_feed = st.toggle("🔴 CONNECT EDGE-NODE (LISTEN TO AGENTS)")

col1, col2, col3 = st.columns([1, 1.2, 1])

with col1:
    st.markdown("#### AGENT 1 • VISION SENTINEL")
    # This text will dynamically update based on what Agent 1 sends via Redis
    st.info(f"📷 Live Detections: {st.session_state.tools}")
    
with col2:
    st.markdown("#### AGENT 2 • VITALS PREDICTIVE ENGINE")
    st.line_chart({"BP_Sys": st.session_state.bp_sys[-20:], "BP_Dia": st.session_state.bp_dia[-20:]}, height=150)
    st.line_chart({"SpO2": st.session_state.spo2[-20:]}, height=150)

with col3:
    st.markdown("#### AGENT 3 • GUARDIAN ALERT LOG")
    st.success("🟢 System Nominal. No alerts.")
    st.markdown("---")
    st.markdown("#### SYSTEM STATUS\n* **Network:** 🟢 AIR-GAPPED & LISTENING")

st.markdown("---")

# --- LLM SUMMARIZER (AGENT 4) ---
col_report, col_btn = st.columns([4, 1])
with col_report:
    st.markdown("#### AGENT 4 • POST-OP EMR SUMMARIZER")
    report_area = st.empty()
    report_area.text_area("Final Clinical Report", value="Awaiting procedure completion...", height=300, disabled=True)

with col_btn:
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("📄 Generate Report"):
        with st.spinner("Compiling Agent Data via Ollama..."):
            full_transcript = " ".join(st.session_state.transcript)
            if not full_transcript:
                full_transcript = "No tools detected during this session."
                
            prompt = f"""
            You are a surgical AI assistant. Write a short, professional Post-Operative Report based strictly on this live surgical event log. 
            SURGICAL LOG: {full_transcript}
            
            POST-OP REPORT FORMAT:
            1. Administrative Overview:
            2. Technical and Safety Log:
            3. Step-by-Step Narrative:
            4. Closure and Dispositions:
            """
            try:
                response = requests.post('http://localhost:11434/api/generate', json={
                    "model": "tinyllama:latest", "prompt": prompt, "stream": False
                }, timeout=30)
                if response.status_code == 200:
                    report_area.text_area("Final Clinical Report", value=response.json()['response'], height=300)
            except Exception as e:
                st.error("Ollama Connection Failed.")

# --- THE REAL-TIME REDIS LISTENER LOOP ---
if live_feed:
    # 1. Ask Redis for one message (Non-blocking)
    message = st.session_state.pubsub.get_message(ignore_subscribe_messages=True)
    
    # 2. If Agent 1 sent a message, unpack the JSON payload
    if message:
        try:
            data = json.loads(message["data"])
            source = data.get('source', 'Unknown')
            event = data.get('event', '')
            
            # Save to transcript for the LLM to read later
            st.session_state.transcript.append(f"[{source}]: {event}")
            
            # If the data came from Agent 1 (Vision), update the UI state
            if source == "Vision":
                st.session_state.tools = event
                
        except json.JSONDecodeError:
            pass # Ignore corrupted packets

    # 3. Wait 0.5 seconds (matching Agent 1's speed) and tell Streamlit to redraw the screen
    time.sleep(0.5)
    st.rerun()