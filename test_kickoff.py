from crewai import Agent, Task, Crew, Process, LLM
import os

# os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
# os.environ["OPENAI_API_KEY"] = "NA"

llm = LLM(model="ollama/llama3:8b", base_url="http://localhost:11434")
agent = Agent(role="Tester", goal="Say hi", backstory="Just a tester", llm=llm, allow_delegation=False)
task = Task(description="Say hi", expected_output="Hi", agent=agent)
crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)

try:
    print("Kicking off...")
    res = crew.kickoff()
    print("Result:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
