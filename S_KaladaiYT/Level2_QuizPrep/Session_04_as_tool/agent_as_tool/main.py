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
    model = "gemini-2.5-flash",
    openai_client = external_client
)

# Weather Agent
weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather agent. You can provide weather information for any location.",
    model=model
)

oba_agent = Agent(
    name="OBAAgent",
    instructions="You are an Osama Bin Adnan agent. Osama is a full stack developer, AI Agentic Developer and Digital Marketer.",
    model=model
)

weather_tool = weather_agent.as_tool(
    tool_name="WeatherTool",
    tool_description="Tool to get the current weather for a given location. Input should be a city name.",
)

oba_tool = oba_agent.as_tool(
    tool_name="OBATool",
    tool_description="Tool to get information about Osama Bin Adnan. Input should be a question about Osama Bin Adnan.",
)

# Create main agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant!",
    model=model,
    # handoffs=[weather_agent, oba_agent],
    tools=[weather_tool, oba_tool],
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "What is current weather in Karachi and who is Osama Bin Adnan?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)