import streamlit as st
import os
import time

# Import the workflow function from main
from main import run_workflow

# 1. Title
st.title("Local Multi-Agent Research Paper Analyzer")

# 2. Short Description
st.write("This system analyzes research paper PDFs using a local multi-agent AI system powered by CrewAI and Ollama.")

# 10. Local Execution Note
st.info("This system runs fully locally using Ollama. No cloud APIs are used.")

# 3. Workflow Section
st.header("Workflow Steps")
st.text("""PDF Upload  
→ Coordinator Agent  
→ Paper Reader Agent  
→ Research Insight Agent  
→ Report Generator Agent  
→ Final Report Output""")

# 4. PDF Upload
st.header("Upload PDF")
uploaded_file = st.file_uploader("Upload a local Research Paper (.pdf)", type=["pdf"])

if uploaded_file is None:
    st.warning("Please upload a PDF file to proceed.")
else:
    # Save the file
    save_path = os.path.join("inputs", "uploaded_paper.pdf")
    if not os.path.exists("inputs"):
        os.makedirs("inputs")
        
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # 5. Analyze Button
    if st.button("Analyze Research Paper"):
        
        # 6. Agent Status Progress
        with st.status("Analyzing Paper...", expanded=True) as status:
            st.write("Coordinator Agent: Validating file")
            time.sleep(0.5)
            st.write("Paper Reader Agent: Extracting text")
            time.sleep(0.5)
            st.write("Research Insight Agent: Analyzing paper")
            time.sleep(0.5)
            st.write("Report Generator Agent: Generating report")
            
            try:
                # Call workflow
                final_state = run_workflow(save_path)
                st.write("Final Report: Ready")
                status.update(label="Analysis Completed Successfully!", state="complete", expanded=False)
                
                # 7. Display Extracted Information
                st.header("Extracted Information")
                
                st.subheader("Paper Title")
                st.write(final_state.get("paper_title", "Not available"))
                
                st.subheader("Objectives")
                objectives = final_state.get("objectives", [])
                if objectives and isinstance(objectives, list):
                    for obj in objectives:
                        st.write(f"- {obj}")
                else:
                    st.write(objectives if objectives else "Not available")
                    
                st.subheader("Methodology")
                st.write(final_state.get("methodology", "Not available"))
                
                st.subheader("Key Findings")
                findings = final_state.get("findings", [])
                if findings and isinstance(findings, list):
                    for find in findings:
                        st.write(f"- {find}")
                else:
                    st.write(findings if findings else "Not available")
                    
                st.subheader("Limitations")
                limitations = final_state.get("limitations", [])
                if limitations and isinstance(limitations, list):
                    for lim in limitations:
                        st.write(f"- {lim}")
                else:
                    st.write(limitations if limitations else "Not available")
                    
                st.subheader("Research Gaps")
                gaps = final_state.get("research_gaps", [])
                if gaps and isinstance(gaps, list):
                    for gap in gaps:
                        st.write(f"- {gap}")
                else:
                    st.write(gaps if gaps else "Not available")
                    
                st.subheader("Future Work")
                future_work = final_state.get("future_work", [])
                if future_work and isinstance(future_work, list):
                    for fw in future_work:
                        st.write(f"- {fw}")
                else:
                    st.write(future_work if future_work else "Not available")
                    
                # 8. Final Report Preview
                st.header("Final Report Preview")
                report_content = final_state.get("final_report", "")
                if report_content:
                    st.markdown(report_content)
                else:
                    st.warning("Report generation yielded no output, display fallback message.")
                
                # 9. Download Button
                final_output_path = final_state.get("output_path", os.path.join("outputs", "final_report.md"))
                
                # Retrieve actual saved content if available
                if os.path.exists(final_output_path):
                    with open(final_output_path, "r", encoding="utf-8") as rf:
                        file_data = rf.read()
                else:
                    file_data = report_content
                
                if file_data:
                    st.download_button(
                        label="Download Generated Report",
                        data=file_data,
                        file_name="final_report.md",
                        mime="text/markdown"
                    )

            except Exception as e:
                status.update(label="Analysis Failed", state="error", expanded=False)
                st.error(f"Analysis encountered an error: {str(e)}")
