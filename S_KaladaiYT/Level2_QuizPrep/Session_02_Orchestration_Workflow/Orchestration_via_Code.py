from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

base_url = os.getenv("BASE_URL")
if not base_url:
    raise ValueError("BASE_URL is not set in environment variables")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)


# Web search agent
web_search_agent:Agent = Agent(
    name="WebSearchAgent",
    instructions=
    """
        You perform a web search and return useful content to fulfill the user's request.
    """,
    model=model,
)

# Data analysis agent
data_analysis_agent:Agent = Agent(
    name="DataAnalysisAgent",
    instructions=
    """
        You analyze data, topic related information, extract insights and return useful insights to fulfill the user's request.
    """,
    model=model,
    
)

# Writer Agent
writer_agent:Agent = Agent(
    name="WriterAgent",
    instructions=
    """
        You write formal, structured report based on provided analysis for the user's request.
    """,
    model=model,
)

web_search_output = Runner.run_sync(
    starting_agent=web_search_agent,
    input="Tell me about LLMs"
)

data_analysis_output = Runner.run_sync(
    starting_agent=data_analysis_agent,
    input= f"Analyze the following content and provide insights:\n{web_search_output.final_output}",
)

writer_output = Runner.run_sync(
    starting_agent=writer_agent,
    input=f"Write a short report based on the following analysis:\n{data_analysis_output.final_output}",
)

print(f"\n[bold green]Final Report:[/bold green]\n[bold blue]{writer_output.final_output}[/bold blue]")