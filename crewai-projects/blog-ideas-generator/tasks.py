from datetime import datetime
from textwrap import dedent
from crewai import Task

class BlogIdeasGeneratorTasks():
	def research_task(self, agent):
		return Task(
			description=dedent(f"""\
				Conduct in-depth research through internet and blogs to identify and analyze
				latest top trending developments in the field of generative AI, Current time is:
				{datetime.now()}. You must pinpointing the most pertinent insights, their 
				potetial use cases and their current limitations.
				You output must be a list of the latest emerging trends in generative AI.
				You must ensure that correct urls are included in the output."""),
			expected_output=dedent("""\
				A list of the latest trends in generative AI.
				The output must be a list of JSON object with the following structure:
				[
					{
						Title: "trend title",
						Url: "trend url eg: https://...",
						Content: "trend content"
					},
					...
				]"""),
			async_execution=True,
			agent=agent
		)

	def summary_and_briefing_task(self, agent, context):
		return Task(
			description=dedent(f"""\
				Given a list of the latest trends and contents in generative AI, develop high-quality,
				informative summary that explain each trend and its key future prospect."""),
			expected_output=dedent("""\
				A well-structured summary document that includes the 5 latest AI trends.
				For each trend include: title, brief summary, urls.
				The output must be in a markdown format and must not contain any additional
				text or explanation, for example:

				<output>
					#1- Title: trend 1 title goes here
					## Summary
					Summary goes here
					### Url
					website link and urls goes here

					....

					#5- Title: trend 5 title goes here
					## Summary
					Summary goes here
					### Url
					website link and urls goes here
				</output>
				"""),
			agent=agent,
			context=context,
			output_file=f"/posts/blog_post_{datetime.now().strftime('%Y-%m-%d %H:%M')}.md"
		)