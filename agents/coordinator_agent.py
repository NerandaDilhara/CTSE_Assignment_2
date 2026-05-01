from crewai import Agent

def get_coordinator_agent(llm):
    """
    Creates and returns the Coordinator Agent.
    Role: Validate inputs and route tasks.
    """
    return Agent(
        role='Coordinator Agent',
        goal='Understand the user request, validate that the input file is a PDF, and route the workflow appropriately.',
        backstory='You are a workflow coordinator specialized in validating input files and managing multi-agent tasks.',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
