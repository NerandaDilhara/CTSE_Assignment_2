# Local Multi-Agent Research Paper Analyzer

## Project Overview

The **Local Multi-Agent Research Paper Analyzer** is a locally running AI-powered system designed to analyze research paper PDFs and generate structured academic summary reports.

The system uses a **multi-agent architecture** where each agent handles a specific task such as PDF reading, insight extraction, and report generation.

⚡ **No paid APIs are used** — all processing runs locally using **Ollama models**.

---

## Problem Statement

Analyzing long research papers manually is time-consuming and inefficient. Extracting key elements such as:

- Objectives  
- Methodology  
- Findings  
- Limitations  
- Research gaps  
- Future work  

requires significant effort.

This system automates that entire workflow using intelligent local AI agents.

---

## Key Features

- 📄 Upload and analyze research paper PDFs  
- 🤖 Multi-agent AI architecture (CrewAI)  
- 🧠 Automatic extraction of research insights  
- 📝 Generates structured academic reports  
- 💻 Runs fully locally using Ollama  
- 📊 CLI + Streamlit UI support  
- 🧪 Unit testing included  
- 📁 Saves output as Markdown report  

---

## Technologies Used

- Python  
- CrewAI  
- Ollama  
- PyPDF2  
- Streamlit  
- Pytest  

---

## System Architecture

This project uses **CrewAI** to coordinate multiple agents.

### Workflow

1. User uploads a research paper PDF  
2. Coordinator Agent validates request  
3. Paper Reader Agent extracts text  
4. Research Insight Agent analyzes content  
5. Report Generator Agent creates report  
6. Report saved in `outputs/`  

---

## Workflow Diagram

```text
User Input / PDF Upload
        ↓
Coordinator Agent
(validate + route task)
        ↓
Paper Reader Agent
(extract text)
        ↓
Research Insight Agent
(analyze content)
        ↓
Report Generator Agent
(generate report)
        ↓
Final Output
(outputs/final_report.md)

project/
│
├── agents/
├── tools/
├── inputs/
├── outputs/
├── logs/
├── tests/
├── app.py
├── main.py
├── requirements.txt
└── README.md

git clone https://github.com/your-username/local-multi-agent-research-paper-analyzer.git
cd local-multi-agent-research-paper-analyzer

Create Virtual Environment
python -m venv venv

Activate Environment
venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Install and Run Ollama
https://ollama.com/

ollama run llama3:8b
ollama run phi3
ollama run qwen2.5:7b

Run the Project (CLI)
python main.py

Run the Frontend
streamlit run app.py
# MultiAgentSystem---CTSE-2
# MultiAgentSystem---CTSE-2
# MultiAgentSystem---CTSE-2
# MultiAgentSystem---CTSE-2
