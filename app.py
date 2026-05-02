import streamlit as st
import os
import time

# Import the workflow function from main
from main import run_workflow

# Must be the first Streamlit command
st.set_page_config(page_title="AI Research Analyzer", page_icon="📑", layout="wide")

# Custom CSS for Glassmorphism and Vibrant Colors
st.markdown("""
<style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700;
    }
    
    /* Custom Title Banner */
    .title-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
    }
    
    .title-text {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    .subtitle-text {
        font-size: 1.3em; 
        color: #94a3b8;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Cards for Extracted Info */
    .info-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 198, 255, 0.4);
    }
    
    .info-card h4 {
        color: #38bdf8;
        margin-top: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 12px;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .info-card ul {
        padding-left: 20px;
    }
    
    .info-card li {
        margin-bottom: 8px;
        line-height: 1.5;
    }
    
    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 30px;
        font-weight: 700;
        font-size: 1.1em;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
    }
    
    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.6);
        color: white;
    }
    
    div.stDownloadButton > button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 30px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    div.stDownloadButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
        color: white;
    }
    
    /* Steps formatting */
    .step-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 30px;
    }
    
    .step-box {
        background: rgba(14, 165, 233, 0.1);
        border-left: 4px solid #0ea5e9;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        font-weight: 500;
        color: #e0f2fe;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: background 0.3s ease;
    }
    
    .step-box:hover {
        background: rgba(14, 165, 233, 0.2);
    }
    
    .step-icon {
        background: #0ea5e9;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9em;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 1. Custom Title Banner
st.markdown("""
<div class="title-container">
    <div class="title-text">✨ Multi-Agent Research Analyzer</div>
    <div class="subtitle-text">Upload a research paper and let our local AI crew extract deep insights, methodology, and limitations. Powered by CrewAI & Ollama.</div>
</div>
""", unsafe_allow_html=True)

st.info("System runs fully locally using Ollama. No cloud APIs are used, ensuring your data remains completely private.")

# 2. Main Layout - Two Columns
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.header("⚙️ Workflow Steps")
    st.markdown("""
    <div class="step-container">
        <div class="step-box"><div class="step-icon">1</div> <b>PDF Upload</b> & Validation</div>
        <div class="step-box"><div class="step-icon">2</div> <b>Coordinator Agent</b> Orchestration</div>
        <div class="step-box"><div class="step-icon">3</div> <b>Paper Reader</b> Text Extraction</div>
        <div class="step-box"><div class="step-icon">4</div> <b>Research Insight</b> Deep Analysis</div>
        <div class="step-box"><div class="step-icon">5</div> <b>Report Generator</b> Output Creation</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a Research Paper (.pdf)", type=["pdf"])
    
with col2:
    if uploaded_file is None:
        st.warning("👈 Please upload a PDF file on the left to begin analysis.", icon="📥")
        # Show a placeholder image or empty state
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; opacity: 0.6; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.1);">
            <h1 style="font-size: 6em; margin-bottom: 0;">📑</h1>
            <h3 style="color: #94a3b8;">Waiting for document...</h3>
            <p style="color: #64748b;">Upload a PDF to see the magic happen</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Save the file
        save_path = os.path.join("inputs", "uploaded_paper.pdf")
        if not os.path.exists("inputs"):
            os.makedirs("inputs")
            
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ File uploaded successfully! Ready for multi-agent analysis.")

        # Analyze Button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Analyze Research Paper"):
            
            # Agent Status Progress
            with st.status("🤖 Agents are working on your paper... (This may take a few minutes)", expanded=True) as status:
                st.write("🔄 **Execution Trace:**")
                
                # Setup custom stdout/stderr redirection
                import sys
                import re
                
                log_container = st.empty()
                
                class StreamlitCapture:
                    def __init__(self, container):
                        self.container = container
                        self.text = ""
                        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                    def write(self, msg):
                        sys.__stdout__.write(msg) # Keep terminal output active
                        clean_string = self.ansi_escape.sub('', msg)
                        if clean_string:
                            self.text += clean_string
                            # Limit text to last 4000 chars to avoid UI lag
                            self.container.code(self.text[-4000:], language="text")
                    def flush(self):
                        sys.__stdout__.flush()

                capture = StreamlitCapture(log_container)
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = capture
                sys.stderr = capture
                
                try:
                    # Call workflow
                    final_state = run_workflow(save_path)
                    
                    # Restore stdout/stderr
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    
                    st.write("✨ **Final Report**: Ready!")
                    status.update(label="🎉 Analysis Completed Successfully!", state="complete", expanded=False)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.header("📊 Extracted Information")
                    
                    # Top Row of info
                    st.markdown(f"""
                    <div class="info-card" style="border-top: 4px solid #38bdf8;">
                        <h4>📝 Paper Title</h4>
                        <p style="font-size: 1.4em; font-weight: 700; color: #f1f5f9;">{final_state.get("paper_title", "Not available")}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Columns for info
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        # Methodology
                        st.markdown(f"""
                        <div class="info-card" style="height: 95%; border-top: 4px solid #a855f7;">
                            <h4>🔬 Methodology</h4>
                            <p style="color: #cbd5e1;">{final_state.get("methodology", "Not available")}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Objectives
                        objs_list = final_state.get("objectives", [])
                        if not isinstance(objs_list, list): objs_list = [objs_list] if objs_list else []
                        objs_html = "".join([f"<li>{obj}</li>" for obj in objs_list]) if objs_list else "<li>Not available</li>"
                        
                        st.markdown(f"""
                        <div class="info-card" style="height: 95%; border-top: 4px solid #ec4899;">
                            <h4>🎯 Objectives</h4>
                            <ul style="color: #cbd5e1;">{objs_html}</ul>
                        </div>
                        """, unsafe_allow_html=True)

                    with info_col2:
                        # Key Findings
                        finds_list = final_state.get("findings", [])
                        if not isinstance(finds_list, list): finds_list = [finds_list] if finds_list else []
                        finds_html = "".join([f"<li>{f}</li>" for f in finds_list]) if finds_list else "<li>Not available</li>"
                        
                        st.markdown(f"""
                        <div class="info-card" style="height: 95%; border-top: 4px solid #10b981;">
                            <h4>💡 Key Findings</h4>
                            <ul style="color: #cbd5e1;">{finds_html}</ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Limitations & Gaps
                        lims_list = final_state.get("limitations", [])
                        if not isinstance(lims_list, list): lims_list = [lims_list] if lims_list else []
                        lims_html = "".join([f"<li>{l}</li>" for l in lims_list]) if lims_list else "<li>None mentioned</li>"
                        
                        gaps_list = final_state.get("research_gaps", [])
                        if not isinstance(gaps_list, list): gaps_list = [gaps_list] if gaps_list else []
                        gaps_html = "".join([f"<li>{g}</li>" for g in gaps_list]) if gaps_list else "<li>None identified</li>"
                        
                        st.markdown(f"""
                        <div class="info-card" style="height: 95%; border-top: 4px solid #f59e0b;">
                            <h4>⚠️ Limitations & 🕳️ Gaps</h4>
                            <p style="color: #e2e8f0; font-weight: bold; margin-bottom: 5px;">Limitations:</p>
                            <ul style="color: #cbd5e1; margin-bottom: 15px;">{lims_html}</ul>
                            <p style="color: #e2e8f0; font-weight: bold; margin-bottom: 5px;">Research Gaps:</p>
                            <ul style="color: #cbd5e1;">{gaps_html}</ul>
                        </div>
                        """, unsafe_allow_html=True)

                    # Future Work Card
                    fw_list = final_state.get("future_work", [])
                    if not isinstance(fw_list, list): fw_list = [fw_list] if fw_list else []
                    fw_html = "".join([f"<li>{fw}</li>" for fw in fw_list]) if fw_list else "<li>Not available</li>"
                    
                    st.markdown(f"""
                    <div class="info-card" style="border-top: 4px solid #3b82f6;">
                        <h4>🚀 Future Work</h4>
                        <ul style="color: #cbd5e1;">{fw_html}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                    # Final Report Expander
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.header("📄 Final Report Preview")
                    report_content = final_state.get("final_report", "")
                    
                    with st.expander("🔍 Click to Expand and View Full Markdown Report", expanded=False):
                        if report_content:
                            st.markdown(report_content)
                        else:
                            st.warning("Report generation yielded no output.")
                    
                    # Download Button
                    final_output_path = final_state.get("output_path", os.path.join("outputs", "final_report.md"))
                    
                    # Retrieve actual saved content if available
                    if os.path.exists(final_output_path):
                        with open(final_output_path, "r", encoding="utf-8") as rf:
                            file_data = rf.read()
                    else:
                        file_data = report_content
                    
                    if file_data:
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Download Generated Report (.md)",
                            data=file_data,
                            file_name="final_report.md",
                            mime="text/markdown"
                        )

                except Exception as e:
                    status.update(label="❌ Analysis Failed", state="error", expanded=False)
                    st.error(f"Analysis encountered an error: {str(e)}")
