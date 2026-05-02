from crewai import LLM
llm = LLM(model="ollama/llama3:8b", base_url="http://localhost:11434")
from agents.coordinator_agent import get_coordinator_agent
try:
    agent = get_coordinator_agent(llm)
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
