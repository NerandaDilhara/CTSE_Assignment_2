import os
import logging
from crewai.tools import tool

def get_task_router_tool(shared_state: dict):
    @tool("task_router_tool")
    def task_router_tool(file_path: str) -> str:
        """
        Validates the PDF file path. 
        Input should be the file path string. 
        Updates the global state based on validity.
        """
        if not file_path:
            return "Error: Missing file path."
        
        if not file_path.endswith('.pdf') and not file_path.endswith('.PDF'):
            return "Error: Invalid file extension. Must be a PDF."
            
        if not os.path.exists(file_path):
            return "Error: File does not exist."
            
        shared_state['file_path'] = file_path
        shared_state['intent'] = 'research_paper_analysis'
        shared_state['status'] = 'validated'
        shared_state['next_agent'] = 'paper_reader_agent'
        
        logging.info("Coordinator Agent started")
        logging.info("File validation successful")
        logging.info("Routing task to Paper Reader Agent")
        
        return "Validation successful. Target routed to Paper Reader Agent."

    return task_router_tool
