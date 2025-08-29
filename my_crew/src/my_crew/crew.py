from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from pydantic import BaseModel
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model=os.environ["MODEL"], api_key=os.environ["GEMINI_API_KEY"])

docs_tool = DirectoryReadTool(directory='./league_table.json')
file_tool = FileReadTool()
search_tool = SerperDevTool()



class PremierLeague(BaseModel):
    teams: list[str]
    matches_no: list[int]
    goals_no: list[int]
    win_no: list[int]
    lose_no: list[int]
    draw_no: list[int]


@CrewBase
class MyCrew():
    """MyCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    @agent
    def data_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['data_collector'],  
            tools=[search_tool],
            verbose=True         
        )

    @agent
    def data_analyist(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyist'],  
            allow_code_execution=True,
            tools=[docs_tool, file_tool],
            verbose=True         
        )
  
    @task
    def data_collector_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_collector_task'],
            output_json=PremierLeague,
            output_file='./league_table.json'  
        )

    @task
    def data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_analysis_task'],
            output_file='report.md'  
        )


    @crew
    def crew(self) -> Crew:
        """Creates the MyCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
