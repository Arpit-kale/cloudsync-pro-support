import streamlit as st
import json
from src.agent import process_chat_message
from dotenv import load_dotenv
load_dotenv()
# Set Page Config
st.set_page_config(
    page_title="CloudSync Pro Support System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS with CSS styling for Dark/Glassmorphism theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;500;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4D96FF 50%, #6BCB77 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #8892B0;
        margin-bottom: 2rem;
    }
    
    /* Persona Badges */
    .persona-badge {
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .persona-technical {
        background: linear-gradient(135deg, #12c2e9 0%, #c471ed 50%, #f64f59 100%);
        color: white;
    }
    
    .persona-frustrated {
        background: linear-gradient(135deg, #FAD961 0%, #F76B1C 100%);
        color: white;
    }
    
    .persona-executive {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    
    .persona-none {
        background: #2D3748;
        color: #A0AEC0;
    }
    
    /* Diagnostics Panel Details */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        backdrop-filter: blur(4px);
        margin-bottom: 1rem;
    }
    
    .metric-title {
        font-size: 0.8rem;
        color: #A0AEC0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    /* Document extracts design */
    .doc-extract {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid #4D96FF;
        padding: 0.8rem;
        margin-bottom: 0.8rem;
        border-radius: 0 8px 8px 0;
    }
    
    .doc-source {
        font-size: 0.75rem;
        font-weight: 700;
        color: #4D96FF;
        margin-bottom: 0.2rem;
    }
    
    .doc-section {
        font-size: 0.8rem;
        font-style: italic;
        color: #A0AEC0;
        margin-bottom: 0.4rem;
    }
    
    /* Chat Bubbles custom aesthetics */
    .chat-bubble {
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    .chat-user {
        background-color: #2D3748;
        border: 1px solid #4A5568;
        color: #FFFFFF;
        border-bottom-right-radius: 4px;
        margin-left: 20%;
    }
    
    .chat-agent {
        background: linear-gradient(135deg, rgba(77, 150, 255, 0.1) 0%, rgba(107, 203, 119, 0.1) 100%);
        border: 1px solid rgba(77, 150, 255, 0.25);
        color: #FFFFFF;
        border-bottom-left-radius: 4px;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_results" not in st.session_state:
    st.session_state.last_results = {
        "persona": None,
        "escalated": False,
        "handoff_summary": None,
        "retrieved_docs": [],
        "retrieved_chunks": [],
        "similarity_score": 0.0
    }

# App Layout
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    # Title Header
    st.markdown('<div class="main-title">CloudSync Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Autonomous AI-Driven Customer Support Dispatcher</div>', unsafe_allow_html=True)
    st.divider()
    
    # Render chat logs
    chat_container = st.container(height=500)
    with chat_container:
        if not st.session_state.messages:
            st.info("👋 Hello! Welcome to CloudSync Pro Customer Support. How can we help you today?")
        else:
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    st.markdown(f'<div class="chat-bubble chat-user"><b>You:</b><br>{content}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble chat-agent">{content}</div>', unsafe_allow_html=True)

    # Chat Input
    query = st.chat_input("Ask a question, report a system problem or enter organization query...")
    
    if query:
        # Save user message to state
        st.session_state.messages.append({"role": "user", "content": query})
        
        # Process query through Agent Orchestrator
        with st.spinner("Classifying query and retrieving database docs..."):
            results = process_chat_message(query, st.session_state.messages[:-1])
            
        # Append response to history
        st.session_state.messages.append({"role": "assistant", "content": results["response"]})
        
        # Store latest run metrics
        st.session_state.last_results = results
        st.rerun()

with col2:
    # Sidebar/Diagnostics Panel title
    st.subheader("⚡ Diagnostic Panel")
    st.divider()
    
    # 1. Detected Persona Section
    current_persona = st.session_state.last_results["persona"]
    if current_persona == "Technical Expert":
        badge_html = '<div class="persona-badge persona-technical">Technical Expert</div>'
    elif current_persona == "Frustrated User":
        badge_html = '<div class="persona-badge persona-frustrated">Frustrated User</div>'
    elif current_persona == "Business Executive":
        badge_html = '<div class="persona-badge persona-executive">Business Executive</div>'
    else:
        badge_html = '<div class="persona-badge persona-none">No Request Yet</div>'
        
    st.markdown("<p style='margin-bottom: 0.3rem; color: #A0AEC0;'>Detected Persona</p>", unsafe_allow_html=True)
    st.markdown(badge_html, unsafe_allow_html=True)
    st.write("")
    
    # 2. Similarity Metric
    score = st.session_state.last_results["similarity_score"]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Semantic Match Score</div>
        <div class="metric-value">{score:.4f}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Expandable retrieved documents extracts
    retrieved_chunks = st.session_state.last_results["retrieved_chunks"]
    retrieved_docs = st.session_state.last_results["retrieved_docs"]
    
    with st.expander("📚 Retrieved Source Metadata & Extract Chunks", expanded=True):
        if not retrieved_chunks:
            st.caption("No context retrieved yet. Send a message to search index.")
        else:
            for idx, (chunk, meta) in enumerate(zip(retrieved_chunks, retrieved_docs), 1):
                st.markdown(f"""
                <div class="doc-extract">
                    <div class="doc-source">🔍 [{idx}] Source File: {meta.get('source')}</div>
                    <div class="doc-section">Section: {meta.get('section')}</div>
                    <div style="font-size:0.9rem;">{chunk[:350]}...</div>
                </div>
                """, unsafe_allow_html=True)
                
    # 4. Red alert for Handoff Summary
    is_escalated = st.session_state.last_results["escalated"]
    handoff_summary = st.session_state.last_results["handoff_summary"]
    
    if is_escalated:
        st.error("⚠️ ESCALATION POLICY TRIGGERED - Human Hand-off Mandatory")
        if handoff_summary:
            st.markdown("**Human Handoff Summary JSON:**")
            st.code(handoff_summary, language="json")
    else:
        st.success("✅ SLA Status: Stable (Autonomous AI Response)")

# Footer
st.divider()
st.caption("CloudSync Pro Support System - Version 1.0.0 (Local Neural Classifier)")
