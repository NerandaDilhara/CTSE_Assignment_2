import logging
from pypdf import PdfReader
from crewai.tools import tool

def get_pdf_reader_tool(shared_state: dict):
    @tool("pdf_reader_tool")
    def pdf_reader_tool(file_path: str) -> str:
        """
        Reads a research paper PDF and extracts its text.
        Pass the valid file path as a string.
        """
        if not file_path:
            return "Error: Missing file path."
            
        try:
            reader = PdfReader(file_path)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
                    
            if not extracted_text.strip():
                return "Error: Empty extracted text."
                
            # Clean text (simple cleaning for broken lines / extra spaces)
            cleaned_text = " ".join(extracted_text.split())
            
            shared_state['extracted_text'] = cleaned_text
            shared_state['page_count'] = len(reader.pages)
            shared_state['extraction_status'] = 'success'
            shared_state['next_agent'] = 'research_insight_agent'
            
            logging.info("Paper Reader Agent extracted text from PDF")
            return f"Successfully extracted {len(reader.pages)} pages of text."
            
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    return pdf_reader_tool
