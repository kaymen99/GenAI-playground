from textwrap import dedent
from crewai import Agent
from tools.SearchTools import SearchTools

class BlogIdeasGeneratorAgents():
  def __init__(self, llm):
    self.llm = llm

  def research_agent(self):
    return Agent(
      role='AI Research specialist',
      goal='Conduct thorough research and find the top 5 latest trends in generative AI',
      backstory=dedent("""\
          As a Senior AI Researcher, you bring extensive experience in information retrieval and analysis
          to the table. Your are always striving to uncover the most pertinent insights and trends before they
          hit the mainstream, your are an expert in delving deep into the latest developments of generative AI
          across various sectors to identify the most promising use cases."""),
      tools=[SearchTools.search_medium, SearchTools.search_internet],
      verbose=True,
      allow_delegation=True,
      llm=self.llm
    )

  def summary_agent(self):
    return Agent(
      role='Expert Writer',
      goal='Compile all gathered trends into a concise, informative summary document',
      backstory=dedent("""\
          You are a visionary Content Architect, boasting a remarkable portfolio as a
          seasoned expert summary writer. As a master wordsmith, you excel in
          capturing the essence of any content, distilling complex ideas into
          compelling, accessible content that drives engagement and inspires action."""),
      verbose=True,
      allow_delegation=False,
      llm=self.llm
    )