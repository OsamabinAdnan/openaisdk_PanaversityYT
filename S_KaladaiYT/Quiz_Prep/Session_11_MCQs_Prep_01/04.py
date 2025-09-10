import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, function_tool,ModelSettings, Handoff
from openai import AsyncOpenAI
from rich import print

load_dotenv()
enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

@function_tool
def get_weather(city:str):
    return f"The weather in {city} is cloudy with 30 C."

@function_tool
def add_numbers(a:int, b:int):
    return a + b

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
        - if user ask for weather, then delegate to weather tool
    """,
    model=model,
    tools=[get_weather, add_numbers],
    # model_settings=ModelSettings(
    #     tool_choice="get_weather",
    # ),
    tool_use_behavior="stop_on_first_tool"
)

result = Runner.run_sync(
    main_agent,
    "Hello!"
)

print(result.final_output)

