from crewai import Agent

def get_paper_reader_agent(llm):
    """
    Creates and returns the Paper Reader Agent.
    Role: Extract text from PDF files.
    """
    return Agent(
        role='Paper Reader Agent',
        goal='Read the research paper PDF, extract plain text, and clean unnecessary spaces and broken lines.',
        backstory='You are a document processing specialist that excels at extracting and cleaning text from PDF research papers.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
