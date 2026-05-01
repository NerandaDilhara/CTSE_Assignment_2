from crewai import Agent

def get_research_insight_agent(llm):
    """
    Creates and returns the Research Insight Agent.
    Role: Analyze text to find core research elements.
    """
    return Agent(
        role='Research Insight Agent',
        goal='Analyze the extracted research paper text to identify its title, objectives, methodology, core findings, limitations, and future work.',
        backstory='You are a sharp academic analyst capable of parsing complex research text into structured insights.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
