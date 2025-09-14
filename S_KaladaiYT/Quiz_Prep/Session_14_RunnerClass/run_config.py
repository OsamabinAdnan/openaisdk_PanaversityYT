from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunContextWrapper, function_tool, ModelSettings, enable_verbose_stdout_logging, RunConfig
from openai import AsyncOpenAI
from rich import print
from dataclasses import dataclass


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

# ||||||||||||||||||||||||| Run Config |||||||||||||||||||||||||

my_config = RunConfig(
    model=model_25,
    model_provider=my_client,
    # tracing_disabled=True,
    model_settings=ModelSettings(
        temperature=0.7
    ),
    trace_include_sensitive_data=True, # By default is True but if we only span but not include sensitive data (e.g. inputs/outputs of tool calls or LLM generations) we can set it to False

)

@function_tool
def get_weather(city:str):
    return f"The weather in {city} is sunny"

@function_tool
def add_two_numbers(num1:int, num2:int):
    return f"The sum of {num1} and {num2} is {num1 + num2}"


main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
    """,
    tools=[get_weather, add_two_numbers],
)

result = Runner.run_sync(
    main_agent,
    "Hello! What is current weather in Karachi, Pakistan? and what is the sum of 10 and 20?",
    run_config=my_config,
)

print(f"\n{result.final_output}\n")
print(my_config.model_settings.temperature)
