from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunContextWrapper, function_tool, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from rich import print

load_dotenv()

# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model_25 = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

model_20 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=my_client,
)

@function_tool
def get_weather(city:str):
    return f"The weather in {city} is sunny"

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
    """,
    model=model_25,
    tools=[get_weather],
)

result = Runner.run_sync(
    main_agent,
    "What is the weather in Lahore!",
    max_turns=1
)

print(f"\n{result.final_output}\n")
