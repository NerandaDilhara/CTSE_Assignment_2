import json
import logging
from crewai.tools import tool

def get_research_insight_tool(shared_state: dict):
    @tool("research_insight_tool")
    def research_insight_tool(json_data: str) -> str:
        """
        Saves the analyzed research insights into the state.
        Input MUST be a valid JSON string with the following string and list values:
        "paper_title", "objectives", "methodology", "findings", "limitations", "research_gaps", "future_work".
        """
        if not shared_state.get('extracted_text'):
            return "Error: empty extracted text."
             
        try:
            data = json.loads(json_data)
        except Exception:
            # We provide a fallback if LLM just sends normal text or failing JSON
            return "Error: Input must be a valid JSON format."
            
        shared_state['paper_title'] = data.get('paper_title', 'Unknown Title')
        shared_state['objectives'] = data.get('objectives', [])
        shared_state['methodology'] = data.get('methodology', '')
        shared_state['findings'] = data.get('findings', [])
        shared_state['limitations'] = data.get('limitations', [])
        shared_state['research_gaps'] = data.get('research_gaps', [])
        shared_state['future_work'] = data.get('future_work', [])
        shared_state['next_agent'] = 'report_generator_agent'
        
        logging.info("Research Insight Agent identified paper insights")
        return "Insights successfully saved. Ready for Report Generator Agent."

    return research_insight_tool
