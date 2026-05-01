import os
import logging
from crewai.tools import tool

def get_report_writer_tool(shared_state: dict):
    @tool("report_writer_tool")
    def report_writer_tool(ignored_string: str) -> str:
        """
        Generates and saves the final markdown report using the shared state.
        Input can be any arbitrary string like 'generate'.
        """
        # The LLM's Report Agent generated a rich Markdown file in final_report during the workflow.
        # We will use that directly instead of assembling empty fields!
        report = shared_state.get('final_report', '# AI Generated Research Report\\n\\nReport could not be finalized.')
        
        output_dir = "outputs"
        output_path = os.path.join(output_dir, "final_report.md")
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                return f"Error: writing to missing directory failed. {e}"
                
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(report)
        except Exception as e:
            return f"Error saving report: {e}"
            
        shared_state['final_report'] = report
        shared_state['output_path'] = output_path
        shared_state['status'] = 'completed'
        
        logging.info("Report Generator Agent saved final report")
        logging.info("Workflow completed successfully")
        
        return f"Report successfully saved to {output_path}."

    return report_writer_tool
