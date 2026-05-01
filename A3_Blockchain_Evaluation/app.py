import streamlit as st

st.set_page_config(
    page_title="DHL Nexus - Supply Chain Evaluation",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS injected via Python/Streamlit for a modern look
st.markdown("""
<style>
    /* Sleek gradient text for main app title */
    .premium-title {
        background: -webkit-linear-gradient(45deg, #4f46e5, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .subtitle {
        color: #94a3b8;
        font-size: 1.2rem;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* Style the metric boxes */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #e2e8f0;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# Main Title Area
st.markdown('<h1 class="premium-title">SupplyNexus Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">System Evaluation for DHL Global Tracking Architecture</p>', unsafe_allow_html=True)

# Dashboard Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Current Model", value="Centralized DB", delta="Vulnerability Risk: High", delta_color="inverse")
with col2:
    st.metric(label="Untrusted Parties", value="14,000+", delta="Suppliers, Ports, Customs", delta_color="off")
with col3:
    st.metric(label="Proposed Model", value="Consortium Chain", delta="Recommended Approach", delta_color="normal")

st.divider()

# Comparative Analysis
st.header("Comparative Analysis")

c1, c2 = st.columns(2)

with c1:
    st.subheader("🔴 Traditional System (Status Quo)")
    st.info("Architecture: Hub-and-Spoke RDBMS Database")
    st.error("**Risks:** Single Point of Failure (SPOF)\n\n**Data:** Siloed across borders\n\n**Integrity:** Poor transparent immutability\n\n**Speed:** Extremely High Throughput")

with c2:
    st.subheader("🟢 Blockchain-Based Architecture")
    st.info("Architecture: Distributed Ledger Technology")
    st.success("**Security:** Distributed Trust via BFT Consensus\n\n**Data:** Cryptographic Immutability across borders\n\n**Integrity:** Absolute peer-to-peer verification\n\n**Speed:** Moderate (Appropriate for scale)")

st.divider()

# Verdict Section
st.header("Final Justification Verdict")

with st.container():
    st.warning("### 🔗 Recommended: Hybrid Consortium Blockchain (Hyperledger Fabric)")
    st.markdown("""
    For global logistics operations involving multiple untrusted stakeholders across international borders—like DHL—a **Consortium Blockchain** is the superior technological requirement over a centralized database.
    
    It definitively acts to resolve data silos and establish trustless verification processes without exposing vital corporate trade secrets to a completely public permissionless network (such as Ethereum).
    """)

with st.sidebar:
    st.title("Download Report")
    st.markdown("The complete academic evaluation report is ready for extraction.")
    
    # Try reading the Report.md file generated previously
    try:
        with open("Report.md", "r", encoding="utf-8") as f:
            report_data = f.read()
            st.download_button(
                label="📥 Download Academic Report (.MD)",
                data=report_data,
                file_name="DHL_Blockchain_Evaluation_Report.md",
                mime="text/markdown"
            )
    except Exception:
        st.error("Report.md file not found in the current directory.")

    st.divider()
    st.caption("CTSE Assignment 03 - Streamlit Evaluation App")
