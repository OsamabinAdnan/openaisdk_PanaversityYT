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

    raise ValueError("Error a gya")


@function_tool
def add_numbers(a: int, b: int):
    """sum the for given number"""
    sum = a + b
    return f"first num is {a} and sec is {b} total {sum}"

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[get_weather, add_numbers],
    model=llm_model,
)


result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi and also what is 5 + 3 ?"
)

print(result.final_output)