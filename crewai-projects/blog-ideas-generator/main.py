from crewai import Crew, Process
from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from dotenv import load_dotenv

from agents import BlogIdeasGeneratorAgents
from tasks import BlogIdeasGeneratorTasks

# load api keys from .env
load_dotenv()

# use local ollama llama3-7b
llm = ChatOpenAI(
      model = "crewai-llama3",
      base_url = "http://localhost:11434/v1",
    )

# # can also use llama3 with Groq API
# # But can face rate limit for token per minute (TPM) used
# llm = ChatGroq(
#         api_key=os.getenv("GROQ_API_KEY"),
#         model="llama3-70b-8192"
#       )

agents = BlogIdeasGeneratorAgents(llm)
tasks = BlogIdeasGeneratorTasks()

# Create Agents
researcher_specialist = agents.research_agent()
expert_writer = agents.summary_agent()

# Create Tasks
research_task = tasks.research_task(researcher_specialist)
summary_and_briefing_task = tasks.summary_and_briefing_task(expert_writer, [research_task])

# Create Crew
crew = Crew(
		 agents=[researcher_specialist, expert_writer],
		 tasks=[research_task, summary_and_briefing_task],
		 process=Process.sequential,
		 max_rpm=10,
		 verbose=2
    )

result = crew.kickoff()

# Print results
print("\n\n################################################")
print("## Here is the result")
print("################################################\n")
print(result)