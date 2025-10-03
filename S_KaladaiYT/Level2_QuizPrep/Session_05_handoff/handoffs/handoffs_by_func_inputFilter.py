from agents import Agent, Runner, OpenAIChatCompletionsModel, SQLiteSession, enable_verbose_stdout_logging, handoff, HandoffInputData, function_tool
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
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

# Weather agent to handle weather-related queries
weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather agent. Always reply the weather in request city is cloudy.",
    model=model,
    handoff_description="Handles weather-related queries",
)


# input filtering for handoff function
def input_filter_data (data:HandoffInputData) -> HandoffInputData:
    return HandoffInputData(
        input_history=data.input_history, # Assistant sees the full history (Hello…, then Who is Osama bin Adnan + weather). | When input_history=(), WeatherAgent does not receive the “Who is Osama bin Adnan and weather in Karachi?” context. It only sees the new items (the Osama tool output). So, the WeatherAgent doesn’t have enough grounding to answer about weather.
        pre_handoff_items=data.pre_handoff_items,
        new_items=data.new_items,
    )

## Handoff function
handoff_func = handoff(
    agent=weather_agent,
    input_filter=input_filter_data,
) 

@function_tool
def osamabinadnan():
    return "Osama bin Adnan is Agentic AI developer."

# Create main agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant!",
    model=model,
    handoffs=[handoff_func], # handoff function added here
    tools=[osamabinadnan] # function tool added here
)

# Temporary history

session = SQLiteSession(session_id="agent_history.db")

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "Hello, how are you?",
    session=session,
)

print("\nCALLING AGENT 1")
print("=" * 50)

print(result.final_output)

result2 = Runner.run_sync(
    agent,
    "Who is Osama bin Adnan and What is today's weather in Karachi?",
    session=session,
)

print("\nCALLING AGENT 2")
print("=" * 50)

print(result2.final_output)