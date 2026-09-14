import streamlit as st
import redis
import json
from datetime import datetime

# Configure the page layout
st.set_page_config(page_title="SurgentAI Prototype", layout="wide", page_icon="🏥")

# Connect to Redis
@st.cache_resource
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)

r = get_redis_client()

# Header
st.title("SurgentAI Prototype")
st.markdown("---")

# Layout: Two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Agent 4 - Post-Op EMR Summarizer")
    
    # Text area to act as the report output
    report_area = st.empty()
    report_area.text_area("Final Report", value="Waiting to generate report...", height=300, disabled=True)

    # The Generate Button
    if st.button("Generate Report", type="primary"):
        # Fetch the simulated transcript (for now, just reading the raw stream)
        # In the future, this is where you'll call Ollama
        report_area.text_area("Final Report", value="Report generation in progress...\n(Ollama integration coming next!)", height=300)

with col2:
    st.subheader("Cross-Agent Overview")
    
    # Simulated Alert Log
    st.markdown("**Alert Log**")
    
    # We use a placeholder to update the log
    log_placeholder = st.empty()
    
    # Fetch recent messages from a Redis list (we'll modify the mock script to use a list)
    # For now, let's display a static placeholder to see the UI layout
    log_placeholder.markdown("""
    * **INFO:** Intervention successful.
    * **CRITICAL:** Active dissection near Anaesthesiologist.
    * **WARNING:** SpO2 falling.
    """)

# System Status Footer
st.sidebar.title("System Status")
st.sidebar.markdown("""
- **Vitals Engine:** ✅ Active
- **Vision Engine:** ✅ Active
- **EMR Summarizer:** ⏳ Waiting
- **Network:** Secure
""")