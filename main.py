import os
import logging
from crewai import Task, Crew, Process

# Tools
from tools.task_router_tool import get_task_router_tool
from tools.pdf_reader_tool import get_pdf_reader_tool
from tools.research_insight_tool import get_research_insight_tool
from tools.report_writer_tool import get_report_writer_tool

# Agents
from agents.coordinator_agent import get_coordinator_agent
from agents.paper_reader_agent import get_paper_reader_agent
from agents.research_insight_agent import get_research_insight_agent
from agents.report_generator_agent import get_report_generator_agent

# Configure logging
if not os.path.exists("logs"):
    os.makedirs("logs")
    
logging.basicConfig(
    filename='logs/agent_trace.log',
    filemode='a',
    format='[%(levelname)s] %(message)s',
    level=logging.INFO
)

# Shared Global State Dictionary
shared_state = {
  "user_query": "",
  "file_path": "",
  "intent": "",
  "status": "",
  "next_agent": "",
  "page_count": 0,
  "extracted_text": "",
  "paper_title": "",
  "objectives": [],
  "methodology": "",
  "findings": [],
  "limitations": [],
  "research_gaps": [],
  "future_work": [],
  "final_report": "",
  "output_path": ""
}

def safe_run_tool(tool_obj, arg):
    # Depending on exactly which CrewAI/LangChain base tool we have, safely call the underlying implementation
    if hasattr(tool_obj, 'func'):
        return tool_obj.func(arg)
    elif hasattr(tool_obj, '_run'):
        return tool_obj._run(arg)
    elif hasattr(tool_obj, 'invoke'):
        return tool_obj.invoke({"file_path": arg} if type(arg)==str and arg.endswith('.pdf') else arg)
    else:
        return tool_obj(arg)

def run_workflow(pdf_path: str):
    from crewai import LLM
    llm = LLM(model="ollama/llama3.2:latest", base_url="http://localhost:11434")
    
    # Initialize Tools
    task_router = get_task_router_tool(shared_state)
    pdf_reader = get_pdf_reader_tool(shared_state)
    research_insight = get_research_insight_tool(shared_state)
    report_writer = get_report_writer_tool(shared_state)
    
    # --- PHASE 1: MANUALLY EXECUTE PRE-AGENT TOOLS ---
    logging.info("Executing Pre-Agent Tools Manually")
    safe_run_tool(task_router, pdf_path)
    safe_run_tool(pdf_reader, pdf_path)
    
    # Check what was gathered
    extracted_text = shared_state.get('extracted_text', '')
    
    # --- PHASE 2: INITIALIZE AGENTS WITHOUT TOOLS ---
    coordinator = get_coordinator_agent(llm)
    reader = get_paper_reader_agent(llm)
    insight = get_research_insight_agent(llm)
    reporter = get_report_generator_agent(llm)
    
    task1 = Task(
        description=f"Acknowledge the research paper located at '{pdf_path}'. Please review that the system has securely routed and validated the payload outside of the agent context.",
        expected_output="Confirmation string acknowledging routing.",
        agent=coordinator
    )
    
    task2 = Task(
        description=f"Process the text that was manually extracted by the prep-system. Text sample:\n{extracted_text[:1500]}...",
        expected_output="Short confirmation summary of the text extraction.",
        agent=reader,
    )
    
    task3 = Task(
        description=f"Analyze this extracted text completely to systematically identify the title, objectives, methodology, key findings, limitations, gaps, and future work:\n\n{extracted_text[:4000]}...",
        expected_output="JSON formatted summary of the scientific insights.",
        agent=insight,
    )
    
    task4 = Task(
        description="Using the scientific insights summary generated in the previous task, compile the findings directly into a clear academic Markdown report.",
        expected_output="The final assembled Markdown report content block.",
        agent=reporter,
    )
    
    crew = Crew(
        agents=[coordinator, reader, insight, reporter],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the Tool-less Agents Execution
    result = crew.kickoff()
    final_output = result.raw if hasattr(result, 'raw') else str(result)
    
    # Output is now ready, update global state
    shared_state['final_report'] = final_output
    
    # Extract insights from task3
    try:
        import json, re
        task3_str = task3.output.raw if hasattr(task3.output, 'raw') else str(task3.output)
        json_match = re.search(r'```json\n(.*?)\n```', task3_str, re.DOTALL)
        
        if json_match:
            data = json.loads(json_match.group(1))
        else:
            # Fallback if no markdown code block is used
            # Try to find the first '{' and last '}'
            start = task3_str.find('{')
            end = task3_str.rfind('}')
            if start != -1 and end != -1:
                data = json.loads(task3_str[start:end+1])
            else:
                data = json.loads(task3_str)
            
        shared_state['paper_title'] = data.get('paper_title', 'Generated Report')
        shared_state['objectives'] = data.get('objectives', [])
        shared_state['methodology'] = data.get('methodology', 'Not available')
        shared_state['findings'] = data.get('findings', [])
        shared_state['limitations'] = data.get('limitations', [])
        shared_state['research_gaps'] = data.get('research_gaps', [])
        shared_state['future_work'] = data.get('future_work', [])
    except Exception as e:
        logging.error(f"Could not parse task3 JSON: {e}")
        shared_state['paper_title'] = "Generated Report"  # Fallback
    
    # --- PHASE 3: MANUALLY EXECUTE POST-AGENT TOOLS ---
    logging.info("Executing Post-Agent Tools Manually")
    safe_run_tool(report_writer, "generate")
    
    return shared_state

