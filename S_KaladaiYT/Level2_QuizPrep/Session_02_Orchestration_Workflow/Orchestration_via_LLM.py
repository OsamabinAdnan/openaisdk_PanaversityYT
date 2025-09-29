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

# Web search agent as tool
web_search_agent_tool = web_search_agent.as_tool(
    tool_name="WebSearchTool",
    tool_description="Useful for performing web searches to gather information about a topic.",
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

# Data analysis agent as tool
data_analysis_agent_tool = data_analysis_agent.as_tool(
    tool_name="DataAnalysisTool",
    tool_description="Useful for analyzing data and extracting insights from provided content.",
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

# Writer Agent as tool
writer_agent_tool = writer_agent.as_tool(
    tool_name="WriterTool",
    tool_description="Useful for writing a structured report based on provided analysis.",
)

# Main Orchestrator Agent
main_agent:Agent = Agent(
    name="MainAgent",
    instructions= # Instructions for the orchestrator agent is most important here because it defines how the orchestration will happen
    """
        - You are an intelligent orchestrator agent that uses other agents as tools to fulfill the user's request.
        - You can use the following tools:
            1. `WebSearchTool:` Useful for performing web searches to gather information about a topic.
            2. `DataAnalysisTool:` Useful for analyzing data and extracting insights from provided content.
            3. `WriterTool:` Useful for writing a structured report based on provided analysis.
        - You must first use the WebSearchTool to gather information, then use the DataAnalysisTool to analyze the gathered information, and finally use the WriterTool to write a report based on the analysis.
        - Always think step-by-step.
    """,
    model=model,
    tools=[web_search_agent_tool, data_analysis_agent_tool, writer_agent_tool],
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="Tell me about LLMs"
)

print(f"\n[bold green]Final Output:[/bold green] {result.final_output}")