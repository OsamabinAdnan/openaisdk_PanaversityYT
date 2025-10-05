import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def get_weather(city:str):
    """get weather for given number"""

    return f"the current weather in {city} is cloudy."


OBA_agent = Agent(
    name="Osama bin Adnan Assistant",
    instructions="""
        You are Osama bin Adnan's assistant. You will answer questions about Osama bin Adnan.
            - Osama bin Adnan AI Agents Developer.
            - He is also certified Digital Marketer.
        """,
    model=llm_model,
    handoff_description="Answer questions about Osama bin Adnan.",
)


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[get_weather],
    handoffs=[OBA_agent],
    model=llm_model,
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi and who is Osama bin Adnan?"
)

print(result.final_output)