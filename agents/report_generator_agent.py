from crewai import Agent

def get_report_generator_agent(llm):
    """
    Creates and returns the Report Generator Agent.
    Role: Output the final structured markdown report.
    """
    return Agent(
        role='Report Generator Agent',
        goal='Generate a structured academic report based on the analyzed research insights and save it as a final output file.',
        backstory='You are a professional report writer that transforms lists of insights into nicely formatted academic markdown reports.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
