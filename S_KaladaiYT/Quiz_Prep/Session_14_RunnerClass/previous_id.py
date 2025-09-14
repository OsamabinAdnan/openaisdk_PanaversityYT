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
    # tools=[get_weather, add_two_numbers],
    model=model_25
)

result1 = Runner.run_sync(
    main_agent,
    "What is the capital of Sweden?",

)

result2 = Runner.run_sync(
    main_agent,
    "In which state in capital present?",
    previous_response_id=result1.last_response_id
)

print(f"\nResponse from 1st run: {result1.final_output}\n")
print(f"\n Response from 2nd run: {result2.final_output}\n")
